import encodings
import os, click, invoke, subprocess, fileinput, shutil
import sys
from types import NoneType
from typing import Any
from dataclasses import dataclass

from tomlkit import string
from .cfp_errors import CfpIOError, CfpInitializationError, CfpNotExecutableError, CfpPermissionDeniedError, CfpRuntimeError, CfpTimeoutError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpValueError
from enum import Enum
from shutil import which
from shlex import shlex, split, join
from pathlib import Path
from ..lib.libcf_api import libcfapi_utils
from . import cfp_context as this


#          ^                                                                Legend:
#          ^                                              ~_ (as a prefix)   =====   conditional attribute       
#          ^                                              #_ (as a prefix)   =====   
#          |
#  has-a = |   /  is-a =  < < < ----

#                   context < < < ----------------------------  test_contest
#                  |      |
#                 |         |
#                |           |
#               |             |
#              |               |
#     environment         ---Runner---
#       |   |            |     |  |   |
#      |    |           |     |   |    |
#     |     |          |     |    |     |
#  Keys  Values       |    Input   |     Job  
#                    |      |   Output    | |
#          corque_board     |    |       |   |
#           (queue)         |   |       |     |
#                        IOBuffer    Shell   #_Task___
#                                            |        |
#                                            |         |
#                 DataStream                 |          |
#                                      cmdModule   #_[cmdmodule.CmdFollower] 
#                                             |           |    |
#                                              |         |      |
#                                               |       |        |
#                                                |  Separator    cmdModule
#                                                 | <_________> | 
#                                                  |           |
#                                                  command, commandFollowerWrapper  
#                                                    |  |
#                                                   |   |
#                                                  |    |
#                                         Executable   args
####  
#
# 
#
# 
#FULL JOB BREAKDOWN:
# 
#
#   |
#   C
#   |
#   p
#   | 
#  pwd && cd /dir/other; sudo cmd -v --list .. | /usr/bin/xargs -f 'oreos first' | tee -a filefile | wc && exec 'sh -c cmd'
#
#  ^^ ??? (Don't even remember adding it. Most likely a half-idea that I jotted down in the closest spot 
#          available in the middle of doing something else)
#
# --------8<------------------------------------------------------------------------------>8--------------
#
#            CfPipeline IO Files: Format & Object Notes:
#
# This section is comprised of 4 main subsections. The first 2 are for the file layout/conventions of an 
# InputFile and the structure of the corresponding InputFile object represented in the CfPipeline sourcecode.
# The last 2 discuss the same 2 topics, but for OutputFiles.
#
#     ~InputFiles: Format ~
#
# All input files will:
#       * have the extension '.cfpin'
#       * possibly contain comments:
#           - these can be on any line by themselves, but cannot prefix or follow valid data on the same line
#           - in this section, when you see 'line N' used, the comment lines are skipped when counting 
#       * end with a blank line
#       * be otherwise made up of _specifiers_ (spec.) and _sections_, which are themselves made up
#*        of specifiers and nested sections a.k.a. subsections. 
#           - Sections: 
#               - a section is defined by including `section_name:` at the current nessting level on its owm
#                 line, just like the 'Sections:' line onr nesting level above this line
#               - every line that is meant to be contained in said section should be nested inside the #   
#                 section. That is, it should all be further indented than the section by one or more 
#                 tab-widths. 
#           - specs.
#               - a specifier is just a set statement of the format `var = val`
#               - notice the spaces. The parser needs to see each spec as 3 space-separated tokens, var, =, & val
#       * include the following metadata:
#           - The InputFile doctype specifier, `!DOCTYPE cfp-fileinput-datadoc`
#           - At least two of the predefined sections for the file.fmt
#               - These are the `file` section, which contains the `fmt` spec., and the `data` section
#           - a format specifier of `FORMAT` on line 1 (Required)
#           - a date on line 2, in the format of `DATE=MMDDYYYY` (Required)
#       * follow on of a few predefined structures: 
#           - the following is the definition of CFP_INPUTFILE_FMT_2, an example of what a predefined
#              structure might look like.
#           - this structure has 3 sections: the two required sections and the `creation` section which 
#              specifies the details related to the file's creation. If you want to define your own input
#              structure, remember that the sections `file` and `data` are both required. they are defined in
#              the base InputParser class from which custom parsers are extended. 
#           - The definition of CFP_INPUTFILE_FMT_2 is as follows (obviously without the #s):
#
# --------8<------------------------------------------------------------------------------>8--------------
#
#  | <--START OF PAGE -- STARTS ON NEXT LINE
#   !DOCTYPE cfp-fileio-datadoc
#   # Comments like this can occupy any line AFTER the doctype definition
#   # Start of the 'file' section. This section gives type and formatting info for the file.
#   File:
#       .type = INFILE
#       .fmt = CFP_INPUTFILE_FMT_2
#       .Perms:
#           .type = OCTAL | STR
#           # This is just regex for a three digit octal number or a linux style perm-string e.g. 'drwxr-xr-x'
#           .value = [1-8]{3} | ['"]d?([r-][w-][x-]){3}['"]
#   Data:
#       .CasesPrecursorLines:
#             # Be sure to wrap any lone ints like this in quotes if you want to feed your data in as the cf 
#             # online judge would.
#             # There should be N back-to-back '.precline = ...' defs, where N is the value of `.num_precursors`.
#             # for this example we will assume that this value is 3. The same goes for all other values starting
#             # with `.num_*s`. The * corresponds to a (usually-)nested spec. for which there should be M defs 
#             # where M is the value of the `num_*s` spec. You'll see what is meant below.
#           .num_precursors = '3'
#           .prec_line = 'lorem ipsum'
#           .prec_line = 'lorem ipsum two' 
#           .prec_line = 'ipsum lorem' 
#       .Cases:
#             # This bool is true if the test case should include a line correponing to Cases.num_cases
#             # If included, it would usually be the 1st line unless precursor lines were defined above
#           .given = bool
#           .num_cases = 'some_int'
#           .Case:
#               .num_lines = 'other_int'
#               .Line:
#                   .num_args = 'third_int'
#                    # pretend num_args for this line was '2'
#                   .arg:
#                       .value = 'lorem'
#                   .arg:
#                       .value = 'ipsum'
#            ...
#   Creation:
#       .date = MMDDYYYY 
#       .author:
#           .name = 'str'
#           .git:
#               .username = 'str'
#               .email
#
# --------8<------------------------------------------------------------------------------>8--------------
# Below is the default layout for the context variables
# --------8<------------------------------------------------------------------------------>8--------------
# :::4:::31:::81::95
# :: USER_HOME_DIR            :: "$HOME"                                        :: homedir    :: "/"    
# :: CFP_CTX_DIR              :: "~home~/.local/"                               :: ctxdir     :: "/"
# :: CFP_TEMPLATES_DIR        :: "~home~/data/templates/"                       :: tempdir    :: "/"
# :: CFP_INPUTFILE_TEXT_FMT_1 :: "tempdir/input_01~ext~"                        :: inp1       :: ""
# :: CFP_INPUTFILE_TEXT_FMT_2 :: "tempdir/input_02~ext~"                        :: inp2       :: ""
# :: CFP_OUTPUTFILE           :: "tempdir/output_01~ext~"                       :: out1       :: ""
# :: CFP_DIFF_FILE            :: "tempdir/diff_01~ext~"                         :: exp1       :: ""
# :: CFP_EXPECTED_FILE        :: "tempdir/expected_01~ext~"                     :: exp1       :: ""
#
#
#
#
#
#
#

########                                                                                         ########
###########################################  ~~~~ ENUMS ~~~~  ###########################################
########                                                                                         ########

class RunType(Enum):
    """
    Description: RunType is an attribute of a runner which determines what happens when its run method is called.
    properties:
        SUBPROCESS: Uses the python3 subprocess module to implement the runner
        SUBPROCESS_LEGACY: Uses the subprocess module, but with methods from its legacy api.
    """
    # TODO:

    # 'asynchronous single-command runner using subprocess api'
    SUBPROCESS = {'description_string': 'subprocess_default', 
                  'topipe': False, 
                  'frompipe': False, 
                  'default_input_src': 'subprocess.STDIN', 
                  'default_output_src': 'subprocess.STDOUT'}
    # 'asynchronous pipe-exit command runner using subprocess api'
    SUBPROCESS_LEGACY = {'description_string': 'subprocess_legacy', 
                         'exec_string': 'subprocess.check_output'}    
    
class ResultResolutionMode(Enum):
    """
    Description: This is meant to be a parameter for functions that configure one or more values that are persisted in the application after the function call finishes. It lets the caller specify how they want that value to be set /given. For example, the function could pass the value to its caller via return stmt, set a class variable, add a kv pair to env_dict, etc. To use, just add a kwarg of `arg: ResultResolutionMode = XXX` to func, where XXXX (the default) is one of the options below.
    """
    # TODO:

    # Resolver should return result in the func return statement.
    RETURN_STATEMENT = '"return {}".format(args[2])'
    INSTANCE_PROPERTY = '"{}({})".format(args[2], args[3])'
    ENV_DICT = '"self.putenv({},{})".format(args[2], args[3])'

    def Resolver(self)->bool:
        exec(self.value)

class IOType(Enum):
    """
    Description: An Enum used for defining whether an IO object is to be used with input or output.
    Values: 
        INPUT: 0
        OUTPUT: 1
    """
    # TODO:

    INPUT = 0
    OUTPUT = 1
    SOURCE = 2

class InputType(Enum):
    """
    properties:
        Enum ([type]): [description]
    """
    # TODO:

    INFILE = 0
    INSTREAM = 1
    INSTRING = 2
    INPIPE = 3

class OutputType(Enum):
    """
    properties:
        Enum ([type]): [description]
    """
    # TODO:

    OUTFILE = 0
    OUTSTREAM = 1
    OUTPIPE = 2

class FileType(Enum):
    """
    properties:
        Enum ([type]): [description]
    """
    # TODO:
    PLAINTEXT_FILE = 00,
    INTS_ONLY_TEXT_FILE = 1
    BINARY_FILE_GENERIC = 2
    # For more info about FILE_FMT_N, see section 'IO File Formats' at the top of this module
    CFP_INPUTFILE_TEXT_FMT_1 = 3
    CFP_INPUTFILE_TEXT_FMT_2 = 4
    CFP_INPUTFILE_BINARY = 5
    CFP_OUTPUTFILE = 6
    CFP_DIFF_FILE = 7
    SOURCE_FILE_GENERIC = 8
    SOURCE_FILE_PY2 = 9
    SOURCE_FILE_PY3 = 10
    SOURCE_FILE_C = 11
    SOURCE_FILE_CPP = 12
    SOURCE_FILE_JAVA = 13
    DIRECTORY = 14


class LanguageChoice(Enum):
    """
    description: a collection of names of programming languages
    properties:
        `Language_name`: each represents a programming language, source code of which is accepted by one of the apis
    """    
    C_SHARP_MONO = 'C#mono',
    D_DMD32 = 'D_DMD32',
    GO = 'Go',
    HASKELL = 'Haskell',
    JAVA_8 = 'Java8',
    JAVA_11 = 'Java11',
    KOTLIN_14 = 'Kotlin1.4',
    KOTLIN_15 = 'Kotlin1.5',
    OCAML = 'Ocaml',
    DELPHI = 'Delphi',
    FREE_PASCAL = 'Free Pascal',
    PASCAL_ABC_DOT_NET = 'PascalABC.NET',
    PERL = 'Perl',
    PHP = 'PHP',
    PYTHON_2 = 'Python2',
    PYTHON_3 = 'Python3',
    PYPY_2 = 'Pypy2',
    PYPY_3 = 'Pypy3',
    RUBY = 'Ruby',
    RUST = 'Rust',
    SCALA = 'Scala',
    JS_V8 = 'JavaScriptV8',
    NODE_JS = 'nodejs'

    def __init__(self):
        super.__init__()

class Openability(Enum):
    """For a file, represents whether or not it can be opened, and usually, the reason."""
    OPENABLE = 0
    NO_FILE = 1
    NOT_OPENABLE = 2
    PROGRAM_NOT_EXECUTABLE = 3
    INSUFFICIENT_PERMISSIONS = 4
    FILETYPE_NOT_SUPPORTED = 5
    NOT_OPENABLE_REASON_UNKNOWN = 6

########                                                                                         ########
########################################  ~~~~ IO_HANDLERS ~~~~  ########################################
########                                                                                         ########    

class IOHandlerBase:
    """
    properties:
        [type]: [description]
    """
    # TODO:

    @property
    def handler_args(self):
        if not self.__hndlr_args:    
            self.__hndlr_args = []
        return self.__hndlr_args

    @handler_args.setter
    def handler_args(self, ls:list):
        self.__hndlr_args = ls

    @property
    def io_type(self)->IOType:
        return self.__io_t

    @io_type.setter
    def io_type(self, iotype: IOType)->None:
        """
        Sets io_type from IOType Enum object. io_type is either INPUT, SOURCE, or OUTPUT, otherwise throw error.
        """
        self.__io_t = iotype

    @io_type.setter
    def io_type_fromstring(self, io_type:IOType):
        """
        Sets io_type from string. io_type is either input, source, or output, otherwise throw error.
        """
        if io_type.lower() == 'i' or io_type.lower() == 'in' or io_type.lower() == 'input':    
            self.__io_t = IOType.INPUT
        elif io_type == 'o' or io_type == 'out' or io_type == 'output':
            self.__io_t = IOType.OUTPUT
        elif io_type.lower() is 's' or io_type.lower() is 'src':
            self.__io_t = IOType.SOURCE
        elif len(io_type) >= 3 and io_type.lower() in 'source':
            self.__io_t = IOType.SOURCE 
        else:
            raise CfpValueError from CfpUserInputError(f'Invalid value given for parameter {io_type}')
        return True

    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            return self
        else:
            self.handler_args = args
            for k,v in kwargs:
                st = f'{k}={v}'
                self.handler_args.append(st)
        return self

class InputHandler(IOHandlerBase):
    """
    Note: Must be run with ContextManager
    Description: An IOHandler subclass set up to feed an input source (params.source)
    """
    # TODO:

    @property
    def input_type(self):
        return self.__inp_t

    @input_type.setter
    def input_type(self,type_str: str)->bool:
        self.__inp_t = type_str    

    def __init__(self, itype: str, *args, **kwargs):
        super().__init__(args, kwargs)
        self.input_type(itype)


class InputFileHandler(InputHandler):
    """
    Description: IOHandler for an input file
    """    
    #TODO: 
    #   Add methods: load_file, handle
    #   Add property: handle_action:
    
    @property
    def current_file(self) -> "this.CfpFile":
        """The current_file property."""
        return self.__f_curr
    
    @current_file.setter
    def current_file(self, value:"this.CfpFile") -> None:
        self.__f_curr = value
    
    @property
    def files_previously_handled(self) -> "list[this.CfpFile]":
        """The files_previously_handled property."""
        return self.__previous_files
    
    @files_previously_handled.setter
    def files_previously_handled(self, value:"list[this.CfpFile]"=None) -> None:
        self.__previous_files = value
    
    @property
    def files_on_deck(self) -> "list[this.CfpFile]":
        """The files_on_deck property."""
        return self.__files_on_deck
    
    @files_on_deck.setter
    def files_on_deck(self, value) -> None:
        self.__files_on_deck = value

    def get_content_from_current(self, format:FileType=FileType.CFP_INPUTFILE_TEXT_FMT_1) -> "this.CfpFile":
        with open(self.current_file) as curr:
            lines = []
            for line in curr:
                lines.append(line)

    def __init__(self, file:"this.CfpFile"=None, *args, **kwargs):
        super().__init__(InputType.INFILE, *args, **kwargs)        

class OutputHandler(IOHandlerBase):
    """
    Description: Active container which implements an interface for controlling what happens to, and what is affected by, the output of a runner in a context.
    """
    # TODO:
    #   - add implementation

    def to_file(self, fullpath, encoding:str="UTF-8")-> None:
        try:
           ofile = open(fullpath, "w", encoding=encoding)
        except IOError:
            raise CfpUserInputError from CfpIOError
        except BaseException as e:
            raise CfpRuntimeError from e

########                                                                                         ########
########################################  ~~~~ RUNNER_SUBS ~~~~  ########################################
########                                                                                         ########     

class InputCommandString(str):
    """
    description: represents a string containing one or more shell commands
    properties:
        shell_lang: see method docstring
    """
    # TODO:

    @property
    def primary_shellchoice(self):
        """
        Description: This is the shell that this object's shellscript code should be evaluated with
        Returns: The shell_lang property's current value
        Defaults to: Bash 
        """
        if not self.__flavor:
            self.__pref_rnr_sh = 'Bash'
        return self.__flavor
    
    @primary_shellchoice.setter
    def primary_shellchoice(self,sh):
        self.__rnr_sh = sh

    def to_cmd_objs(self):
        """
        Description: This method converts the method to a list of Command objects.
        Returns: 
        """
        pass 


class Program(Path):
    """
    Description: Represents a running instance of a computer program.
    properties: 
        operating_system (str): The os on which the program is running
        invoked_by (str): The username of the account that the program was executed under.
        fullpath (str): full path to the program's executable file.
    """
    # TODO:
    
    @property
    def operating_system(self) -> str:
        """The os on which the program is running."""
        return self.__op_sys
    
    
    @operating_system.setter
    def operating_system(self, o_s:str=None) -> None:
        if o_s is None:
            self.__op_sys = sys.platform
        else:
            self.__op_sys = o_s
    
    @property
    def invoked_by(self)-> str:
        """The username of the account that the program was executed under"""
        return self.__caller
    
    @invoked_by.setter
    def invoked_by(self, user:str=None)-> None:
        if user is None:
            self.__caller = str(os.path.expandvars('$USER'))
        elif type(user) == str:
            self.__caller = user
        else:
            raise CfpTypeError()
            
    @property
    def fullpath(self)-> Path:
        return self.__full_path
    
    @fullpath.setter
    def fullpath(self, val:str)-> None:
        if type(val) is str:
            self.__full_path = Path(val)
        elif type(val) is Path:
            self.__full_path = val
        else:
            raise CfpTypeError

    def __init__(self, name_or_path:str):
        p = super().__init__(name_or_path)
        if not p.exists:
            self.fullpath(shutil.which(p))
            if self.fullpath() == None:
                raise CfpNotExecutableError
            try:
                o_p = open(p)
            except PermissionError:
                raise CfpPermissionDeniedError
            self.fullpath(name_or_path)
            
    def run(self,shell_errors_fail:bool=False):
        """
        Description: A very simple builtin runner that runs the program without args and returns the output. No option for pipes, etc.
        Raises:
            CfpPermissionDeniedError: User doesn't have permissions required to run the specified program
            CfpTimeoutError: Process did not return within the allotted time
            CfpRuntimeError: Catchall for any other runtime errors
        Returns:
            str: process output
        """
        try:
            r_p = subprocess.run(self.fullpath, capture_output=True)
        except PermissionError:
            raise CfpPermissionDeniedError
        except subprocess.TimeoutExpired:
            raise CfpTimeoutError
        except subprocess.SubprocessError:
            raise CfpRuntimeError
        else:
            if str(r_p.returncode) != '0':
                if shell_errors_fail == True:
                    print(str('Cfp Runtime Exception: process returned with status ', r_p.returncode, ' and message ', r_p.stderr))
                    raise CfpRuntimeError
                else:
                    print(str('Process returned with status ', r_p.returncode, ' and message ', r_p.stderr))
            else:
                return str(r_p.stdout)


class CmdArg(str):

    """
    properties:
        [type]: [description]
    """
    # TODO:

    def __init__(self, input_src):
        super().__init__(input_src)

    def as_str(self):
        try:
            return str(self)
        except BaseException as e:
            raise CfpRuntimeError from e

    def as_int(self):
        try:
            return int(self)
        except BaseException as e:
            raise CfpRuntimeError from e


class CmdArgString(str):    
    """
    properties:
        [type]: [description]
    """
    # TODO:

    def __init__(self, *args):
        super().__init__(args)

class CmdArgList:
    """
    properties:
        args: the actual arguments list. Type is list[CmdArg]
    """
    # TODO:

    @property
    def args(self)-> "list[CmdArg]":
        return self.__args

    @args.setter
    def args(self,*args)-> None:
        a_ls = []
        for arg in args:
            if type(arg) is CmdArg():
                a_ls.append(arg)
            elif type(arg) is str or type(arg) is int:
                a_ls.append(CmdArg(str(arg)))
            elif type(arg) is list or type(arg) is tuple:
                for i in arg:
                    a_ls.append(CmdArg(str(i)))
        self.__args = a_ls

    @property
    def args_count(self)-> int:
        if not self.__args():
            return 0
        else:
            return len(self.__args)

    def to_argstring(self):
        a_str = ''
        for a in self.args:
            if a_str == '':
                a_str = a
            else:
                a_str = a_str + ' ' + a
        else:
            if a_str == '':
                return None
            else:
                return a_str.lstrip().rstrip()

    def __addlist(self, ls: list):
        if type(ls) is not list:
            raise CfpTypeError
        else:
            for i in ls:
                self.__args.append(CmdArg(i))

    def __addtuple(self, tup:tuple):
        if type(tup) is not tuple:
            raise CfpTypeError
        else:
            for i in tup:
                self.__args.append(CmdArg(str(i)))            

    def __addint(self, i:int):
        if type(i) is not int:
            raise CfpTypeError
        else:
            self.__args.append(CmdArg(str(i)))

    def __addstring(self, s:str):
        if type(s) is not str and type(s) is not string:
            raise CfpTypeError
        else:
            self.__args.append(CmdArg(str(s)))

    def __addcmdarg(self, a:CmdArg):
        if type(a) is not CmdArg:
            raise CfpTypeError
        else:
            self.__args.append(a)

    def __init__(self, *input):
        for i in input:
            if type(i) is CmdArg:
                self.__addcmdarg(i)
            if type(i) is list:
                self.__addlist(i)
            elif type(i) is tuple:
                self.__addtuple(i)
            elif type(i) is int:
                self.__addint(i)
            elif type(i) is str or type(i) is string:
                self.__addstring(i)
            else:
                raise CfpTypeError

class Command:
    """
    properties:
        [type]: [description]
    """
    # TODO:

    @property
    def executable(self)-> Program:
        return self._exec

    @executable.setter
    def executable(self, prog:Program)-> str:
        self.__exec = prog

    @property
    def args(self)-> list:
        return self.__args
    
    @args.setter
    def args(self, *args)-> None:
        try:
            arg_ls = []
            for arg in args:
                arg_ls.append(arg)
            self.__args = arg_ls
        except TypeError:
            raise CfpTypeError
        except ValueError:
            raise CfpValueError
        except BaseException as e:
            raise CfpRuntimeError from e

    def __init__(self, exe:Program, *args):
        self.executable(exe)
        self.args(args)


@dataclass
class CfpFile:
    """
    Base class for Executable, Source_File, Shell_Application, Input_File, and anything with a location: Path attribute. Not all will be eligible for File.open(), as directories are files as well.  
    """    
    # TODO:

    @property
    def handler(self)-> IOHandlerBase:
        return self.__handler

    @handler.setter
    def handler(self, handler)-> None:
        self.__handler = handler

    @property
    def location_path(self)-> Path:
        if type(self.__loc) is Path:
            return self.__loc
        else:
            raise CfpTypeError

    @location_path.setter
    def location_path(self, loc:Path)-> None:
        if type(loc) is Path:
            self.__loc = loc
        else:
            raise CfpTypeError

    @property
    def filetype(self)-> FileType:
        return self.__f_type

    @filetype.setter
    def filetype(self, ftype:FileType)-> None:
        self.__f_type = ftype

    @property
    def size_in_bytes(self)-> int:
        return self.__num_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, bytes:int)-> None:
        self.__num_bytes = bytes

    @property
    def is_openable(self,)-> bool:
        if type(self.__can_open) is bool:
            return self.__can_open
        else:
            raise CfpTypeError
    
    @is_openable.setter
    def is_openable(self,o:bool)-> None:
        if type(o) is bool:
            self.__can_open = o
        else:
            raise CfpTypeError

    def content(self):
        if self.__f_type() is FileType.CFP_INPUTFILE_TEXT_FMT_1:
            lines_list = []
            with open(self.location_path()) as c:
                count = 0
                for line in c:
                    count = count + 1
                    lines_list.append((int(count), str(line))) 

    def get_template(self, loc):
        pass

    def from_scratch(self, header):
        pass
        

class Task:
    """
    Represents a group of one or more commands connected together via pipes / fifos. IMPORTANT: commands which are connected via `&&` , `||` , or `;` are not 
    """
    # TODO:

    content:"list[Command]" = None
    
    def __init__(self):
        pass
              
class ShellProgram(Program):
    """
    Description: A program that starts a command shell when run. e.g. bash, cmd, etc.  
    Propertiess:
        name: a string version of the program name. Often the last part of the path.
        launchpath: the path to the launch prog. Usually 
    Methods:
        run: start the program via the launchpath
    """
    @property
    def name(self):
        return self.__namestr
    
    @name.setter
    def name(self, arg):
        self.__namestr = arg
        
    @property
    def launchpath(self):
        return self.__launch_path
    
    @launchpath.setter
    def launchpath(self, lp: Path):
        self.__launch_path = lp
        
    @property
    def command_concat(self):
        """
        This string is used to concat the command strings. Expects values such as '&&'.
        """
        return self.__cmd_concat
    
    @command_concat.setter
    def command_concat(self, val):
        self.__cmd_concat = str(val)
        
    def __init__(self, name:str, concat:str, altpath:Path=None):
        self.name(name)
        self.command_concat(concat)
        self.launchpath(altpath)
        super().__init__()
        
    def run_task(self, task:Task):
        if self.launchpath is not None:
            callstr = str(self.launchpath(), ' ', task.as_string(self.command_concat()))
        else:
            callstr = str(self.path, ' ', task.as_string(self.command_concat()))
        output = subprocess.run(callstr)
    
    def run_task_via_progpath_call(self, task:Task):
        callstr = str(self.path, ' ', task.as_string(self.command_concat()))
        sub = subprocess.run(callstr)

class Job:
    """
    Description: Abstraction for a job of the format 'run specified list of commands using specified program' assigned to a runner
    Params:
            top_level -- constant -- boolean -- if true, this Job is meant for running lower level jobs. If false, it is a lower_level itself, and is for running Task lists
    """
    # TODO:

    TOP_LEVEL:bool = False
    
    @property
    def aliases(self) -> "list[str]":
        return self.__aliases
    
    @aliases.setter
    def aliases(self, vals:"list[str]") -> None:
        self.__aliases = vals    
    
    @property
    def content(self) -> "tuple[ShellProgram,Task]":
        return self.__content
    
    @content.setter
    def content(self, tup) -> None:
        if type(tup) == tuple and len(tup) == 2: 
            if type(tuple[1]) is Task:
                self.__content = tup  
            else:
                raise CfpTypeError
        else: 
            raise CfpTypeError
    
    def __init__(self, *cmd_ls:Task, aliases:list):
        if len(cmd_ls) <= 0:
            raise CfpUserInputError('Job objects must always contain at least one Task.')
        else:
            self.content = cmd_ls
    
    def to_string(self):
        try:
            progpath = which(str(self.content[0]))
            cmd_str = ' '.join(list(self.self.content[1]))
            return progpath + cmd_str
        except TypeError:
            raise CfpTypeError
        except BaseException as e:
            print("invoked by ", str(e))
            raise CfpRuntimeError
        
########                                                                                         ########
##########################################  ~~~~ RUNNERS ~~~~  ##########################################
########                                                                                         ########

@dataclass
class BaseRunner:
    """
    Description: This class should be a relative of EVERY runner defined in the application. It defines only logic that must be present for all runners, and therefore lays out the minimal contract for this abstraction.

    Properties:
        infile: pathlib.Path
            Path: path to the input file for this runner
        infrom:
            InputHandler: The runner's input source 
        outto:
            OutputHandler: The runner's output source 
        job:
            Job: The current job assigned to the runner
    """
    # TODO:

    @property
    def infile(self)->InputHandler:
        return self.__input_file

    @infile.setter
    def infile(self, arg)->None:
        self.__input_file = arg

    @property
    def infrom(self)->str:
        return self.__in_from

    @infrom.setter
    def infrom(self, arg)-> None:
        self.__in_from = arg

    @property
    def outto(self)-> OutputHandler:
        if type(self.__out_to) == OutputHandler:
            return self.__out_to
        else:
            raise TypeError

    @outto.setter
    def outto(self, dest)-> None:
        self.__out_to = dest

    @property
    def job(self, arg)-> Job:
        return self.__cmd_list

    @job.setter
    def job(self, clist)-> None:
        self.__cmd_list = clist

    def __init__(self, in_from=None, out_to=None, infile=None, cmd=None):
        self.infrom(in_from) 
        self.outto(out_to)
        self.infile(infile) 
        if self.infile and self.infrom:
            raise CfpUserInputError("You cannot specify values for both input and infile")
        elif self.infile:
            pth = Path(self.infile)
            if Path.exists(pth):
                self.in_from = fileinput(pth)
            else:
                raise CfpUserInputError("If included, value for infile must be a valid path")        
             

    def InitializeIOHandler(self, *handler_args, **handler_kwargs):
        """
        Description: creates and returns an IOHandler with 
        Args:
            handler_args: tuple
            handler_kwargs: tuple

        Raises:
            CfpUserInputError: Raised if the data given to the instance is invalid
            IOError: Called as a parent of the first Error
            CfpInitializationError: Raised if a system error is caught upon init of the link

        Returns:
            IOHandler: This class is responsible for the IO of its Runner. May be InputIOHandler or OutputIOHandler
        """
        if self.infile():
            handler = IOHandlerBase(self.infile(), handler_args)
        return handler

class CfpRunner(BaseRunner):
    """
    Description: This is a highly dynamic class which is responsible for nearly all cfp runner types. If the init method is called directly, it will raise an error, but the various runner-type-getters, e.g. get_new_*_runner(), call init after setting a class property. After this is set, the runner will build itself according to its value.
    
    Properties:
      runtype_old: 
    """
    # TODO: 
    
    DEFAULT_INPUT_SRC = 'subprocess.STDIN'
    DEFAULT_OUTPUT_SRC = 'subprocess.STDOUT'
    __r_type_old = ''

    @property
    def frompipe(self) -> bool:
        return self.__frompipe

    @frompipe.setter
    def frompipe(self, frm: bool) -> None:
        self.__frompipe = frm

    @property
    def topipe(self) -> bool:
        return self.__topipe

    @topipe.setter
    def topipe(self, to_pipe:bool) -> None:
        self.__topipe = to_pipe

    @property


    @property
    def argstring(self) -> CmdArgString :
        return self.__argstring

    @argstring.setter
    def argstring(self, arg_str:Any) -> None :
        try:
            if type(arg_str) == CmdArgString:
                self.__argstring = arg_str
            elif type(arg_str) == this.CmdArglist:
                cal = ''
                for a in arg_str:
                    cal = cal + str(a) + ' '
                self.__argstring = CmdArgString(str(cal).rstrip())
                # above: cal should be a string already, but it is re-stringified just in case...
            elif type(arg_str) == CmdArg:
                # this should work every time, because CmdArg type is a subtype of str, but it excepts TypeErrors regardless
                self.__argstring = CmdArgString(str(arg_str))
            elif type(arg_str) == str:
                self.__argstring = CmdArgString(arg_str)
            else:
                hailmary = CmdArgString(arg_str)
                if type(hailmary) == CmdArgString:
                    self.__argstring = hailmary
                else:
                    raise TypeError
        except TypeError:
            raise CfpTypeError
        except RuntimeError:
            exc = str(type(e))
            print('Runtime Error: ', exc, ' raised by the back end application.')
            raise CfpRuntimeError
        except BaseException as e:
            exc = str(type(e))
            print('Compiletime Error: ', exc, ' raised by the back end application.')
            raise CfpRuntimeError

    def __init__(self, runtype:RunType, topipe:bool=False, frompipe:bool=False):
        if not self.runtype():
            raise CfpInitializationError("You cannot invoke this __init__() method directly. Try using one of the @classmethods defined by this class to get a new instance.")
        elif self.runtype() == RunType.SUBPROCESS:
            self.strategy = 'subprocess_run'
        elif self.runtype() == RunType.SUBPROCESS_LEGACY:
            self.strategy = 'subprocess_check_output'      
        self.frompipe(frompipe)
        self.topipe(topipe)

    def configure(self):
        pass
    
    @classmethod
    def subprocess_runner(self, legacy:bool=False):
        """
        Description: What it says. It returns a fresh instance of CfpRunner with the Runtype set to SUBPROCESS.   
        """
        if legacy == True:
            self.setRuntype(RunType.SUBPROCESS_LEGACY)
        else:
            self.setRuntype(RunType.SUBPROCESS)
        self.__init__()

    @property
    def runtype(self)-> RunType:
        return self.__invoc_type

    @runtype.setter
    def runtype(self, rt: RunType)-> bool:
        try:
            if self.__r_type:
                self.__r_type_old = self.__r_type
            self.__r_type = rt
        except BaseException as e:
            # TODO: add custom error handling
            raise e
        return True

    def __subprocrun_rnr_run_cmdstring(command_string, ):
        try:
            subprocess.run(command_string,)
        except subprocess.SubprocessError:
            print('Something went wrong. Check input and "try" again.')

########                                                                                         ########
##########################################  ~~~~ CONTEXTS ~~~~  ##########################################
########                                                                                         ########

@dataclass
class Context:
    """
    Description: Base for all contexts. 
    """
    # TODO:
        # Add __enter__() & __exit__() methods to each context subtype
            # if method doesnt finish due to crash, __exit__() needs to write a log entry into the .exceptilog file in the $CTX_DATA_DIR/log/ directory.
            # Both methods should come after __init__() at the end of the class.
                # If __init__() is not already the last method, move it.

    def __enter__(self):
        pass
    
    def __exit__(self):
       pass    

    @property
    def namespace(self)->str:
        return self.__name_space

    @namespace.setter
    def namespace(self, ns:str)->None:
        self.__name_space = ns

    @property
    def ctx_type(self)->str:
        return self.__ctx_t

    @ctx_type.setter
    def ctx_type(self, ctxtype: str)->None:
        self.__ctx_t = ctxtype 

    @property
    def env_dict(self)->dict:
        return self.__environ_dict

    @env_dict.setter
    def env_dict(self, ed: dict, overwrite: bool=False) -> None:
        if self.__environ_dict:
            if len(self.__environ_dict) == 0:
                self.__environ_dict = ed
            elif overwrite == True:
                self.__environ_dict = ed
            elif overwrite == False:
                raise CfpOverwriteNotAllowedError
                   
    def putenv(self,k, v):
        self.env_dict().update({k: v})
        return True
            
    def getenv(self, key):
        return self.env_dict[key]
    
    def get_info(self,outputFmt:str):
        """
        TODO: make sure this is tested with a populated env_dict.
        """
        print.format('CURRENT CONTEXT:' )
        print.format('        Instance of Type:   {} Context', self.ctx_type)
        print.format('    Ctx Namespace Prefix:   {}_')
        print.format('    Ctx Inner Environment: {')
        for k,v in self.env_dict().items():
            if type(v) == str:
                print(f'              {k}: {v}')
            else:
                print(f'              {k}: {str(v)}')           

class CfpShellContext(Context):
    """
    Description: This is a context for running commands in a shell such as bash or zsh. The bash process is run on top of a Python process with its own environment that is kept seperate from the process environment by default, but whose variables can be accessed in the same way as process envvars at context runtime.    
    """
    # TODO:

    def __enter__(self):
       pass
   
    def __exit__(self):
      pass    

    @property
    def shellchoice(self) -> ShellProgram:
        return self.__shell_choice

    @shellchoice.setter
    def shellchoice(self, choice=None) -> None:  
        self.__shell_choice = choice

    @property
    def current_shell(self) -> ShellProgram:  
        return self.__current_shell

    @current_shell.setter
    def current_shell(self, curr=None) -> None:  
        self.__current_shell = curr
        
    def __init__(self, cmds, runner: CfpRunner, shell_env: str, **envvars):
        """
        Description: Init calls parent init (sets namespace, ctx_type) and updates virtual_environment. Sets `cmds_fmt` to a 2d list where each outer element represents a command, itself represented by the inner list, with cmd[0] being the command and the rest of the inner list is its args. 
        """
        super().__init__('shell_ctx','shell')
        self.env_dict.update(envvars)
        self.shellpath = self.check_for_preferred_shell(self.shellchoice, resolve_mode="returnstatement")
    
    def check_for_preferred_shell(self, shellpref:str):
        """
        Description: runs which command with shellname as argument. If cmd returns empty, self.shellpref_avail is set to False and this func returns False. otherwise,it is set to True, and func returns the path which the os uses to execute it, usually "$PREFIX/bin/shellname".
        """
        sh_path = shutil.which(shellpref)
        if sh_path is not None:
            return Path(sh_path)
        else:
            return False

    def run_ctx(self,shellpath_clean):
        self.__run_jobs_with_runner(self.job_runner, shellpath_clean)        
        
    def __run_jobs_with_runner(self, job_runner: CfpRunner, shellpath: str):
        """
        Description: simply runs cmd using self.shellpref. self.shellpref_avail must be True. DO NOT SET IT YOURSELF! To set it, you must first run the check_for_preferred_shell() func above. If it is False, then the shell isn't installed on the current system. In this case 
        """
        pass       

    def __prep_commands_list(self, cmd_list:"list[str]", shellpath):
        self.cmds_fmt = list()
        for c_str in cmd_list:
            for cmd in c_str:
                if type(cmd) == list:
                    self.cmds_fmt.append(cmd)
                elif type(cmd) == str:
                    spl = shlex(cmd)
                    spl.whitespace_split = True
                    self.cmds_fmt.append(list(spl))   

    def __prep_commands_str(self, cmd_str:str, shellpath):
        cmds_ls = cmd_str.split('&&')
        self.__prep_commands_list(cmds_ls,shellpath)
                
class DynamicStrRunnerContext(Context): 
    """
    Description: Sets up the runner based on the value of ctx_type in the parent. Uses concept known as reflection in Java via running eval(runner_str) where runner str is based on ctx_type. This lets us dynamically build a string and then run that string as python3 code. e.g. say ctx_type is "subprocess". The resulting runner_str would be "subprocess.run(cmd)". 
    """
    # TODO:

    def __enter__(self):
       pass
   
    def __exit__(self):
       pass    
    
class CfpShellBasedTestContext(CfpShellContext):
    """
    Description: Context for testing potential Codeforces solutions in a shell context
    """
#   TODO:
#       - fix_me!
#           - multiple lang get/set implementations intermingled
#           - needs only one
#           - allowedlangs needs moved to enum 

    cf_allowedlangs = ['C#mono',
                        'D_DMD32',
                        'Go',
                        'Haskell',
                        'Java8',
                        'Java11',
                        'Kotlin1.4',
                        'Kotlin1.5',
                        'Ocaml',
                        'Delphi',
                        'Free Pascal',
                        'PascalABC.NET',
                        'Perl',
                        'PHP',
                        'Python2',
                        'Python3',
                        'Pypy2',
                        'Pypy3',
                        'Ruby',
                        'Rust',
                        'Scala',
                        'JavaScriptV8',
                        'nodejs'
                       ]
    
    @property
    def solutions_testrunner(self): 
        if not self.__cfp_runner:
            return None
        elif issubclass(type(self.__cfp_runner), BaseRunner) or isinstance(type(self.__cfp_runner), BaseRunner):
            return self.__cfp_runner
        else:
            raise TypeError

    @solutions_testrunner.setter
    def solutions_testrunner(self, rnr):
        if issubclass(type(rnr), BaseRunner) or isinstance(type(rnr), BaseRunner):
            self.__cfp_runner = rnr
        else:
            raise CfpTypeError
    
    # represents the chosen language's index in the cf_allowedlangs list 
    @property
    def cf_lang_index(self)-> int:
        lc = LanguageChoice()
        if not self.__lang_ndx:
            self.__lang_ndx = -1
        elif type(self.__lang_ndx) != int:
            raise CfpTypeError
        elif self.__lang_index >= len(lc):
            raise CfpValueError()
        return self.__lang_ndx

    @cf_lang_index.setter
    def cf_lang_index(self, num: int):
        if type(num) is int:
            self.__lang_ndx = num
        else:
            try:
                self.__lang_ndx = int(num)
            except TypeError:
                raise CfpTypeError
            except ValueError:
                raise CfpValueError
            except BaseException as e:
                print('raised by {}'.format(e))
                raise RuntimeError

    @property
    def lang(self)-> str:
        return self.__lang

    @lang.setter
    def lang(self,lng)->None:
        self.__lang = lng
        return None

    def setlang(self, language:LanguageChoice):
        """
        Description: Believe it or not, this one sets the lang
        """
        for i,lang_option in enumerate(self.cf_allowedlangs):
            if lang_option.lower() in '_'.join(list(map(str, language.split(' ')))).lower():
                self.cf_lang_index = i
                break
            elif self.default_lang:
                if self.cf_lang_index < 0:
                    raise IOError('You must provide a language!')
            else:    
                lang = self.cf_allowedlangs[language]
                self.putenv('solutionlanguage', lang)



    def __init__(self, cmds, rnnr: CfpRunner, shell_env: str, language: str, **envvars: any):
        super().__init__(cmds, rnnr,  envvars)
        self.setlang(language)


