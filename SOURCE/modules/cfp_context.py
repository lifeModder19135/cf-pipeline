import encodings
import os, click, invoke, subprocess, fileinput, shutil
import sys
# from types import NoneType
from typing import Any, List, Tuple, Union
from dataclasses import dataclass

# from tomlkit import string
from SOURCE.modules.cfp_errors import CfpIOError, CfpInitializationError, CfpNotExecutableError, CfpPermissionDeniedError, CfpRuntimeError, CfpTimeoutError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpValueError
from enum import Enum, Flag
from shutil import which
from shlex import shlex, split, join
from pathlib import Path, PosixPath, WindowsPath
from SOURCE.lib.libcf_api import libcfapi_utils
from SOURCE.lib.libcfp_maintutils import PathFinder
# from . import cfp_context as this


#          ^                                                                Legend:
#          ^                                              ~_ (as a prefix)   =====   conditional attribute       
#          ^                                              #_ (as a prefix)   =====   
#          |
#  has-a = |   /  is-a =  < < < ----

#                   context < < < ----------------------------  test_context
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
# All input, output, or expected format 1 files will:
#       * have the extension '.cfpin', '.cfpout', or '.cfpexp'
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
#           - The definition of CFP_INPUTFILE_FMT_1 is as follows (obviously without the #s):
#
# --------8<------------------------------------------------------------------------------>8--------------
#
#  | <--START OF PAGE -- STARTS ON NEXT LINE
#   !DOCTYPE cfp-fileio-datadoc
#   # Comments like this can occupy any line AFTER the doctype definition
#   # Start of the 'file' section. This section gives type and formatting info for the file.
#   File:
#       .type = INFILE
#       .fmt = CFP_INPUTFILE_FMT_1
#       .perms:
#           .type = OCTAL | STR
#           # This is just regex for a three digit octal number or a linux style perm-string e.g. 'drwxr-xr-x'
#           .value = [1-8]{3} | ['"]d?([r-][w-][x-]){3}['"]
#   Data:
#       .casesPrecursorLines:
#             # Be sure to wrap any lone ints like this in quotes if you want to feed your data in as the cf 
#             # online judge would.
#             # There should be N back-to-back '.precline = ...' defs, where N is the value of `.num_precursors`.
#             # for this example we will assume that this value is 3. The same goes for all other values starting
#             # with `.num_*s`. The * corresponds to a (usually-)nested spec. for which there should be M defs 
#             # where M is the value of the `num_*s` spec. You'll see what is meant below.
#           .numPrecursors = '3'
#           .precLine = 'lorem ipsum'
#           .precLine = 'lorem ipsum two' 
#           .precLine = 'ipsum lorem' 
#       .cases:
#             # This bool is true if the test case should include a line corresponding to Cases.num_cases
#             # If included, it would usually be the 1st line unless precursor lines were defined above
#           .given = bool
#           .numCases = 'some_int'
#           .case:
#               .line:
#                   .value = 'lorem'
#                   .value = 'ipsum'
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

class RunType(Flag):
    """
    RunType is an attribute of a runner which determines what happens when its run method is called.
    properties:
        SUBPROCESS: Uses the python3 subprocess module to implement the runner
        SUBPROCESS_LEGACY: Uses the subprocess module, but with methods from its legacy api.
    """
    # TODO:

    # 'asynchronous single-command runner using subprocess api'
    SUBPROCESS_RUN = {'description_string': 'subprocess_default', 
                  'topipe': False, 
                  'frompipe': False, 
                  'default_input_src': 'subprocess.STDIN', 
                  'default_output_src': 'subprocess.STDOUT'}
    # 'asynchronous pipe-exit command runner using subprocess api'
    SUBPROCESS_RUN_LEGACY = {'description_string': 'subprocess_legacy', 
                         'exec_string': 'subprocess.call'}   

    SUBPROCESS_POPEN = {'description_string': 'subprocess_popen', 
                         'exec_string': 'subprocess.Popen'}
    
    SUBPROCESS_CHECKOUTPUT = {'description_string': 'subprocess_check_output', 
                         'exec_string': 'subprocess.check_output'}
    
class ResultResolutionMode(Flag):
    """
    This is meant to be a parameter for functions that configure one or more values that are persisted in the application after the function call finishes. It lets the caller specify how they want that value to be set /given. For example, the function could pass the value to its caller via return stmt, set a class variable, add a kv pair to env_dict, etc. To use, just add a kwarg of `arg: ResultResolutionMode = XXX` to func, where XXXX (the default) is one of the options below.
    """
    # TODO:

    # Resolver should return result in the func return statement.
    RETURN_STATEMENT = '"return {}".format(args[2])'
    INSTANCE_PROPERTY = '"{}({})".format(args[2], args[3])'
    ENV_DICT = '"self.putenv({},{})".format(args[2], args[3])'

    def Resolver(self) -> bool:
        exec(self.value)

class IOType(Flag):
    """
    A Flag used for defining whether an IO object is to be used with input or output.
    Values: 
         INPUT: object is to be used with input
        OUTPUT: object is to be used with output
        SOURCE: object is to be used with source code
    """
    # TODO:

    INPUT = 0
    OUTPUT = 1
    SOURCE = 2

class InputType(Flag):
    """
    A flag with values representing different input sources.
    Values: 
        INFILE: data is coming from a file
        INSTREAM: data is coming from a stream
        INSTRING: data is coming from a Python string
        INPIPE: data is coming from a pipe
    """
    # TODO:

    INFILE = 0
    INSTREAM = 1
    INSTRING = 2
    INPIPE = 3

class OutputType(Flag):
    """
    A flag used in OutputHandler with values representing different output sources.
    Values:
        OUTFILE: handler is outputting to a file
        OUTSTREAM: handler is outputting to a stream
        OUTPIPE: handler is outputting to a pipe
    """
    # TODO:

    OUTFILE = 0
    OUTSTREAM = 1
    OUTPIPE = 2

class FileType(Flag):
    """
    Represents different types of files.
    """
    # TODO:
    PLAINTEXT_FILE = 00,
    INTS_ONLY_TEXT_FILE = 1
    BINARY_FILE_GENERIC = 2
    # For more info about FILE_FMT_N, see section 'IO File Formats' at the top of this module
    CFP_INPUTFILE_TEXT_FMT_1 = 3
    CFP_INPUTFILE_TEXT_FMT_2 = 4
    CFP_INPUTFILE_BINARY = 5
    CFP_OUTPUTFILE_TEXT_FMT_1 = 6
    CFP_EXPECTEDFILE_TXT_FMT_1 = 7
    SOURCE_FILE_GENERIC = 8
    SOURCE_FILE_PY2 = 9
    SOURCE_FILE_PY3 = 10
    SOURCE_FILE_C = 11
    SOURCE_FILE_CPP = 12
    SOURCE_FILE_JAVA = 13
    DIRECTORY = 14

class LanguageChoice(Flag):
    """
    A collection of names of programming languages. Each represents a programming language, source code of which is accepted by one of the apis
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

    # def __init__(self):
    #     super.__init__()

class Openability(Flag):
    """For a file, represents whether or not it can be opened, and usually, the reason."""
    OPENABLE = 0
    NO_FILE = 1
    NOT_OPENABLE = 2
    PROGRAM_NOT_EXECUTABLE = 3
    INSUFFICIENT_PERMISSIONS = 4
    FILETYPE_NOT_SUPPORTED = 5
    NOT_OPENABLE_REASON_UNKNOWN = 6

class Separator(Flag):
    """A list of possible command line Separators such as '&&' and '|' that connect commands in various ways."""
    AMPERSANDS = '&&'
    PIPE = '|'
    DOUBLE_PIPE = '||'
    FORWARD_FIFO = '>'
    BACKWARD_FIFO = '<'
    SEMICOLON = ';'

########                                                                                         ########
########################################  ~~~~ IO_HANDLERS ~~~~  ########################################
########                                                                                         ########    

class IOHandlerBase:
    """
    A base class for all InputHandlers and OutputHandlers. These store data for input and output sources. This class itself is not to be invoked. To use it, instantiate one of it's subclasses.
    properties:
        handler_args: arguments passed to handler
        io_type: either input or output
    """
    # TODO:

    @property
    def handler_args(self) -> List:
        """arguments passed to the handler"""
        return self.__hndlr_args
        
    @handler_args.setter
    def handler_args(self, ls:list) -> None:
        self.__hndlr_args = ls

    @property
    def io_type(self) -> IOType:
        """Must be set to either IOType.SOURCE, IOType.INPUT or IOType.OUTPUT"""
        return self.__io_t
        
    @io_type.setter
    def io_type(self, iotype) -> None:
        """
        Sets io_type from IOType Enum object. io_type is either INPUT, SOURCE, or OUTPUT, otherwise throw error.
        """
        if type(iotype) == IOType:
            self.__io_t = iotype
        elif type(iotype) == str:
            if str(iotype).lower() == 'i' or str(iotype).lower() == 'in' or str(iotype).lower() == 'input':    
                self.__io_t = IOType.INPUT
            elif str(iotype).lower == 'o' or str(iotype).lower == 'out' or str(iotype).lower == 'output':
                self.__io_t = IOType.OUTPUT
            elif str(iotype).lower() == 's' or str(iotype).lower() == 'src':
                self.__io_t = IOType.SOURCE
            elif len(str(iotype)) >= 3 and str(iotype).lower() in 'source':
                self.__io_t = IOType.SOURCE 
            else:
                raise CfpValueError('Invalid value given for parameter iotype') from CfpUserInputError('Invalid value given for parameter iotype')
            return True
        else:
            raise CfpValueError from CfpUserInputError('The value provided for io_type must be of type string or IOType.')

    def __init__(self, args: list, io_type: IOType = None, str_io_type: str = None) -> None:
        """
        sets io_type and handler_args
        """
        if io_type != None and str_io_type != None:
            raise CfpValueError from CfpUserInputError('io_type and str_io_type cannot both have values. Ohe or the other.')
        elif io_type != None or str_io_type != None:
            self.io_type = io_type
        else:
            raise CfpValueError from CfpUserInputError('You must provide a value for either io_type or str_io_type.')
        self.handler_args = args

class InputHandler(IOHandlerBase):
    """
    Holds data about the input of a runner in a context.
    """
    # TODO:

    __inp_t: InputType

    @property
    def io_type(self) -> IOType:
        """Hard coded to IOType.INPUT"""
        return self.__io_t
    
    @io_type.setter
    def io_type(self) -> None:
        raise CfpOverwriteNotAllowedError('io_type is hardcoded to INPUT and cannot be changed.') 

    @property
    def input_type(self) -> InputType:
        """must be set to a value of type InputType"""
        return self.__inp_t

    @input_type.setter
    def input_type(self, itype: InputType) -> None:
        if type(itype) == InputType:
            self.__inp_t = itype
        else:
            raise CfpTypeError from CfpUserInputError('The type of itype must be InputType.')   

    def __init__(self, itype: InputType, args: List):
        self.__io_t = IOType.INPUT
        self.handler_args = args
        self.input_type = itype

    def __enter__():
        pass

    def __exit__():
        pass

@dataclass
class CfpFile:
    """
    Base class for Executable, Source_File, Shell_Application, Input_File, and anything with a location: Path attribute. Not all will be eligible for File.open(), as directories are files as well. If location_path does not point to an actual file, object will still be built, but size_in_bytes will be 0 and is_openable will be false.  
    """    
    # TODO:

    __loc: Path
    __f_type: FileType
    __num_bytes: int
    __can_open: bool

    @property
    def location_path(self) -> Path:
        """This holds the full absolute path to this file"""
        if type(self.__loc) is PosixPath or type(self.__loc) is WindowsPath:
            return self.__loc
        else:
            raise CfpTypeError

    @location_path.setter
    def location_path(self, loc:Path) -> None:
        if type(loc) is PosixPath or type(loc) is WindowsPath:
            self.__loc = loc
        else:
            raise CfpTypeError

    @property
    def filetype(self) -> FileType:
        """This describes the type of file. It is set to a value of this module's FileType flag."""
        return self.__f_type

    @filetype.setter
    def filetype(self, ftype:FileType) -> None:
        self.__f_type = ftype

    @property
    def size_in_bytes(self) -> int:
        """As it says, this is an int describing the size of the file in bytes"""
        return self.__num_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, bytes:int) -> None:
        self.__num_bytes = bytes

    @property
    def is_openable(self,) -> bool:
        """This is a boolean denoting whether or not the file can be opened."""
        if type(self.__can_open) is bool:
            return self.__can_open
        else:
            raise CfpTypeError
    
    # @is_openable.setter
    # def is_openable(self,o:bool) -> None:
    #     if type(o) is bool:
    #         self.__can_open = o
    #     else:
    #         raise CfpTypeError
        
    def __init__(self, loc: Path, ftype: FileType):
        self.location_path = loc
        self.filetype = ftype
        if type(self.location_path) == PosixPath or type(self.location_path) == WindowsPath:
            self.__set_size()
        else:
            raise CfpTypeError('param `loc` must be a Path object')
        try:
            os.stat(self.location_path)
            with open(self.location_path, 'r'):
                self.__can_open = True
        except FileNotFoundError:
            self.__can_open = False
        except PermissionError:
            self.__can_open = False
        


    def __set_size(self):
        try:
            stats = os.stat(self.location_path)
            size = stats.st_size
            self.size_in_bytes = size
        except FileNotFoundError:
            self.size_in_bytes = 0

    def get_content(self) -> list:
            if self.__f_type() is FileType.CFP_INPUTFILE_TEXT_FMT_1:
                lines_list = []
                if os.path.isfile(self.location_path) == True:
                    with open(self.location_path()) as c:
                        count = 0
                        for line in c:
                            count = count + 1
                            lines_list.append((int(count), str(line)))
                        return lines_list
                else:
                    raise CfpValueError('self.location_path must point to a valid file.')

    @classmethod
    def get_template(self, loc):
        """Not yet implemented. This will be a class method that gets a template from <path>, copy that template, and load it as a file to be edited."""
        pass

    @classmethod
    def from_scratch(self, header):
        """Not yet implemented. This will be a class method that builds a cfp formatted file from scratch."""
        pass

class InputFileHandler(InputHandler):
    """
    InputHandler for an input file
    """    
    #TODO: 
    #   Add methods: load_file, handle
    #   Add property: handle_action:

    __f_curr: CfpFile
    __previous_files: List[CfpFile]
    __files_on_deck: List[CfpFile]

    @property
    def current_file(self) -> CfpFile:
        """The current_file being handled."""
        return self.__f_curr
    
    @current_file.setter
    def current_file(self, value:CfpFile) -> None:
        self.__f_curr = value
    
    @property
    def files_previously_handled(self) -> List[CfpFile]:
        """A queue of files that have already been used."""
        return self.__previous_files
    
    @files_previously_handled.setter
    def files_previously_handled(self, value: List[CfpFile]=None) -> None:
        self.__previous_files = value
    
    @property
    def files_on_deck(self) -> List[CfpFile]:
        """The files_to be loaded after the current file is finished."""
        return self.__files_on_deck
    
    @files_on_deck.setter
    def files_on_deck(self, value) -> None:
        self.__files_on_deck = value

    def get_content_from_current(self, format: FileType = FileType.CFP_INPUTFILE_TEXT_FMT_1) -> list:
        """This returns the content of the current file as a list of lines."""
        with open(self.current_file.location_path) as curr:
            return curr.readlines()
           
    def pipe_input_file(inputfile):
        """pipes an input file from param into current_file"""
        pass

    def parse_inputfile():
        """parses an input file and returns a list of input data"""

    def __init__(self, files: List[CfpFile], args: List = None):
        super().__init__(InputType.INFILE, args)
        self.current_file = files[0]
        self.files_previously_handled = []
        self.files_on_deck = files[1:]

    def __enter__():
        pass

    def __exit__():
        pass

class OutputHandler(IOHandlerBase):
    """
    Holds data about the output of a runner in a context.
    """
    # TODO:
    #   - add implementation

    __outtype_: OutputType

    @property
    def io_type(self):
        """Hard coded to IOType.OUTPUT"""
        return self.__io_t

    @io_type.setter
    def io_type(self, x):
        raise CfpOverwriteNotAllowedError('io_type is hardcoded to OUTPUT and cannot be changed.')

    @property
    def output_type(self) -> OutputType:
        """This describes the type of output it is working with. The content must be of type OutputType"""
        return self.__outtype_
    
    @output_type.setter
    def output_type(self, ot: OutputType) -> None:
        self.__outtype_ = ot

    @property
    def content(self) -> List:
        """This holds the content of the output source."""
        return self.__content
    
    @content.setter
    def content(self, cont: list) -> None:
        self.__content = cont

    def __init__(self, outputtype: OutputType, args: List):
        self.__io_t = IOType.OUTPUT
        self.output_type = outputtype
        self.handler_args = args


    def to_file(self, fullpath, encoding:str="UTF-8") -> None:
        try:
           ofile = open(fullpath, "w", encoding=encoding)
        except IOError:
            ofile.close()
            raise CfpUserInputError from CfpIOError
        except BaseException as e:
            ofile.close()
            raise CfpRuntimeError from e
        
    def __enter__():
        pass

    def __exit__():
        pass

########                                                                                         ########
########################################  ~~~~ RUNNER_SUBS ~~~~  ########################################
########                                                                                         ########     

class InputCommandString:
    """
    This represents a string containing one or more shell commands.
    """
    # TODO:

    __rnr_sh: str
    __command: str

    @property
    def primary_shellchoice(self) -> str:
        """
        This is the shell that this object's shellscript code should be evaluated with
        Defaults to: 'bash' or 'cmd'
        """
        return self.__rnr_sh
    
    @primary_shellchoice.setter
    def primary_shellchoice(self, sh: str = 'bash') -> None:
        self.__rnr_sh = sh

    @property
    def command(self) -> str:
        """This holds the actual command or commands as a string"""
        return self.__command
    
    @command.setter
    def command(self, comm) -> None:
        self.__command = comm

    def __init__(self, cmd, shell: str = None):
        if shell == None:
            if os.name == 'posix':
                self.primary_shellchoice = 'bash'
            elif os.name == 'nt':
                self.primary_shellchoice = 'cmd'
            else:
                self.primary_shellchoice = None
        else:
            self.primary_shellchoice = shell
        self.command = cmd

    def to_cmd_objs(self):
        """
        Not yet implemented. This method will convert the command string to a list of Command objects. 
        """
        pass 

class Program:
    """
    Represents a running instance of a computer program.
    properties: 
        operating_system (str): The os on which the program is running
        invoked_by (str): The username of the account that the program was executed under.
        fullpath (str): full path to the program's executable file.
    """
    # TODO:

    __op_sys: str
    __caller: str
    __full_path: Union[PosixPath, WindowsPath]
    
    @property
    def operating_system(self) -> str:
        """The os on which the program is running. If not specified during initialization, it defaults to your current operating system."""
        return self.__op_sys
    
    
    @operating_system.setter
    def operating_system(self, o_s:str) -> None:
        self.__op_sys = o_s
    
    @property
    def invoked_by(self) -> str:
        """The username of the account that the program was executed under. If not given during initialization, it defaults to the current user."""
        return self.__caller
    
    @invoked_by.setter
    def invoked_by(self, user:str=None) -> None:
        self.__caller = user
            
    @property
    def fullpath(self) -> Path:
        """This is the full absolute path to the program, including the file name"""
        return self.__full_path
    
    @fullpath.setter
    def fullpath(self, val: Union[str, PosixPath, WindowsPath]) -> None:
        if type(val) is str:
            self.__full_path = Path(val)
        elif type(val) is PosixPath or type(val) is WindowsPath:
            self.__full_path = val
        else:
            raise CfpTypeError('The value of must be a string or a pathlib.Path object')

    def __init__(self, path: Path, opsys: str = None, caller: str = None):
        if opsys == None:
            self.operating_system = str(os.name)
        else:
            self.operating_system = opsys
        if caller == None:
            self.invoked_by = str(os.path.expandvars('$USER'))
        else:
            self.invoked_by = caller
        self.fullpath = path
            # try:
            #     o_p = open(p)
            # except PermissionError:
            #     raise CfpPermissionDeniedError
            # self.fullpath(name_or_path)

    def tostring(self):
        """Returns a string representation of the path to the program. <fullpath> attribute must be set for this to work."""
        return str(self.fullpath)
            
    def run(self,shell_errors_fail:bool=False) -> str:

        """
        A very simple builtin runner that runs the program without args and returns the output. No option for pipes, etc.
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

class CmdArg:

    """
    A single argument or option to a single command.
    """
    # TODO:

    __arg: str

    @property
    def argument(self) -> str:
        """The argument itself"""
        return self.__arg
    
    @argument.setter
    def argument(self, a: str) -> None:
        self.__arg = a

    def __init__(self, input_src):
        self.argument = input_src

    def as_str(self) -> str:
        """This returns the argument as a string"""
        try:
            return str(self)
        except BaseException as e:
            raise CfpRuntimeError from e

    def as_int(self) -> int:
        """This tries to return the argument as an integer. If it fails, s CfpRuntimeError will be raised."""
        try:
            return int(self)
        except BaseException as e:
            raise CfpRuntimeError from e

class CmdArgString(str):
    """
    This is a string containing one or more command arguments. Should contain all arguments and options given to a single command. In other words, the entire command line minus the command itself. For all arguments in list form, see CmdArgList.
    """
    # TODO:

    def __new__(cls, value, *args, **kwargs):
        return super(CmdArgString, cls).__new__(cls, value)

class CmdArgList:
    """
    A list of CmdArg objects representing all options and arguments of a single command line, along with some metadata about the list.
    properties:
        args: the actual arguments list. Type is list[CmdArg]
    """
    # TODO:

    __args: List

    @property
    def args(self) -> List[CmdArg]:
        """This holds the actual arguments list. Type is list[CmdArg]"""
        return self.__args

    @args.setter
    def args(self,*args) -> None:
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
    def args_count(self) -> int:
        """This holds the amount of arguments and/or options in the list."""
        return len(self.__args)

    def tostring(self) -> str:
        """This returns a string representation of the arguments / options stored here, as they would be listed on the command line."""
        a_str = ''
        for a in self.args:
            if a_str == '':
                a_str = a.argument
            else:
                a_str = a_str + ' ' + a.argument
        else:
            if a_str == '':
                return None
            else:
                return a_str.lstrip().rstrip()

    def addlist(self, ls: list) -> None:
        """This adds a list of args, in string form to the list. It first converts them to CmdArg objects, then it adds them to the list."""
        if type(ls) is not list:
            raise CfpTypeError
        else:
            for i in ls:
                self.__args.append(CmdArg(i))

    def addtuple(self, tup:tuple) -> None:
        """This adds a tuple of args, in string form to the list. It first converts them to CmdArg objects, then it adds them to the list."""
        if type(tup) is not tuple:
            raise CfpTypeError
        else:
            for i in tup:
                self.__args.append(CmdArg(str(i)))            

    def addint(self, i:int) -> None:
        """This converts a single int argument into a CmdArg object and adds it to the list."""
        if type(i) is not int:
            raise CfpTypeError
        else:
            self.__args.append(CmdArg(str(i)))

    def addstring(self, s:str) -> None:
        """This converts a single string argument into a CmdArg object and adds it to the list."""
        if type(s) is not str and type(s) is not str:
            raise CfpTypeError
        else:
            self.__args.append(CmdArg(str(s)))

    def addcmdarg(self, a:CmdArg) -> None:
        """This adds a single CmdArg to the list."""
        if type(a) is not CmdArg:
            raise CfpTypeError
        else:
            self.__args.append(a)

    def __init__(self, input: Union[CmdArg, List, tuple, int, str]):
        self.__args = []
            
        if type(input) == CmdArg:
            self.addcmdarg(input)
        elif type(input) == list:
            self.addlist(input)
        elif type(input) == tuple:
            self.addtuple(input)
        elif type(input) == int:
            self.addint(input)
        elif type(input) == str:
            self.addstring(input)
        else:
            # print(type(i))
            raise CfpTypeError(type(input))

class CommandLine:
    """
    This holds a single command line. Here, a command line is a command with it's associated arguments and/or options.
    """
    # TODO:

    __exec: Program
    __args: CmdArgList

    @property
    def executable(self) -> Program:
        """This holds the base command of the command line."""
        return self.__exec

    @executable.setter
    def executable(self, prog: Program) -> str:
        self.__exec = prog

    @property
    def args(self) -> CmdArgList:
        """This is a list of all arguments and/or options associated with the command line, in the order that they appear."""
        return self.__args
    
    @args.setter
    def args(self, args: CmdArgList) -> None:
        if type(args) == CmdArgList:
            self.__args = args
        else:
            raise CfpTypeError
        # try:
        #     arg_ls = []
        #     for arg in args:
        #         arg_ls.append(arg)
        #     self.__args = arg_ls
        # except TypeError:
        #     raise CfpTypeError
        # except ValueError:
        #     raise CfpValueError
        # except BaseException as e:
        #     raise CfpRuntimeError from e

    def __init__(self, exe:Program, args: CmdArgList):
        self.executable = exe
        self.args = args

    def tostring(self):
        """This returns the command line in string form."""
        str1 = self.executable.tostring()
        str2 = self.args.tostring()
        str3 = str1 + ' ' + str2
        return str3

class Task:
    """
    This represents a group of one or more command lines connected together via pipes / fifos. IMPORTANT: There must be the same amount of items in the 'Separators' list as their are in the 'content' list, otherwise the functions of this class will produce errors!
    """
    # TODO: add tostring method which combines the content and Separators into a string that can be run on the command line

    __content: List[CommandLine]
    __seps: List[Separator]

    @property
    def content(self) -> List[CommandLine]:
        """
        A list containing the command lines to be connected. The length of this list must be the same lingth as the separators list.
        """
        return self.__content
    
    @content.setter
    def content(self, c: List[CommandLine]) -> None:
        self.__content = c 

    @property
    def separators(self) -> List[Separator]:
        """
        a list of Separators (i.e. '&&' of '|') that separate the command lines in 'content', in the order that they appear. The amount of separators must be the same as the amount of CommandLine objects in 'content', and the last item must be Separator.SEMICOLON. 
        """
        return self.__seps
    
    @separators.setter
    def separators(self, s: List[Separator]) -> None:
        self.__seps = s

    def __init__(self, content: List[CommandLine], separators: List[Separator]):
        self.content = content
        self.separators = separators

    def tostring(self):
        """This returns a string representation of the task, which itself can be run via a command prompt."""
        if len(self.content) == len(self.separators):
            string = ''
            zipped = zip(self.content, self.separators)
            for c,s in zipped:
                string = string + c.tostring()
                if s == Separator.AMPERSANDS:
                    string = string + ' && '
                elif s == Separator.BACKWARD_FIFO:
                    string = string + ' < '
                elif s == Separator.DOUBLE_PIPE:
                    string = string + ' || '
                elif s == Separator.FORWARD_FIFO:
                    string = string + ' > '
                elif s == Separator.PIPE:
                    string = string + ' | '
                elif s == Separator.SEMICOLON:
                    string = string + '; '
                else:
                    raise CfpTypeError('The "separators" list must only contain values of type Separator.')
            return string.lstrip(' ').rstrip(' ')
        else:
            raise CfpUserInputError('The list length of "content" must equal the list length of "separators".')

class ShellProgram(Program):
    """
    A program that starts a command shell when run. e.g. bash, cmd, etc.  
    Propertiess:
        name: a string version of the program name. Often the last part of the path.
        launchpath: the path to the launch prog. Usually 
    Methods:
        run: start the program via the launchpath
    """
    @property
    def name(self) -> str:
        """The name of the shell. e.g. 'bash'"""
        return self.__namestr
    
    @name.setter
    def name(self, arg) -> None:
        self.__namestr = arg
        
    @property
    def launchpath(self) ->Path:
        """the path to the executable. e.g. '/bin/bash'; This only needs set if it is different than fullpath, such as if it uses an alias."""
        return self.__launch_path
    
    @launchpath.setter
    def launchpath(self, lp: Path) -> None:
        self.__launch_path = lp
        
    def __init__(self, sp_name: str, sp_fullpath: Path, sp_launchpath: Path = None, sp_opsys: str = None, sp_caller: str = None):
        super().__init__(sp_fullpath, opsys=sp_opsys, caller=sp_caller)
        self.name = sp_name
        self.launchpath = sp_launchpath
        
    def run_task(self, task:Task) -> None:
        """This runs a task with the shell via invoking launchpath <launchpath>"""
        if self.launchpath is not None:
            callstr = str(str(self.launchpath), ' ', task.tostring())
        else:
            callstr = str(str(self.path), ' ', task.tostring())
        output = subprocess.run(callstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return output
    
    def run_task_via_progpath_call(self, task:Task) -> None:
        """Just like <run_task>, this runs a task with the shell, butinstead of using <launchpath>, this invokes <fullpath>."""
        callstr = str(str(self.path), ' ', task.tostring())
        sub = subprocess.run(callstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

class Job:
    """
    This is an abstraction for a job of the format 'run specified list of commands using specified program' assigned to a runner
    Params:
            top_level -- constant -- boolean -- if true, this Job is meant for running lower level jobs. If false, it is a lower_level itself, and is for running Task lists
    """
    # TODO:

    TOP_LEVEL: bool
    
    @property
    def aliases(self) -> dict:
        """a dictionary where the keys are strings representing aliases and the values are strings representing what they expand to."""
        return self.__aliases
    
    @aliases.setter
    def aliases(self, vals: dict) -> None:
        self.__aliases = vals    
    
    @property
    def content(self) -> Tuple:
        """the task to be run and the shell to run it with"""
        return self.__content
    
    @content.setter
    def content(self, lst: list) -> None:
        if type(lst) == list: 
            if len(lst) == 2: 
                if type(lst[0]) == ShellProgram and type(lst[1]) == list:
                    self.__content = lst  
                else:
                    raise CfpTypeError('One or more items inside tuple is of the wrong type. This must be a tuple containing a ShellProgram instance and a list of Task objects, in that order.')
            else:
                raise CfpUserInputError('Tuple more of less than 2 items. This must be a tuple containing a ShellProgram instance and a list of Task objects, in that order.')
        else: 
            raise CfpTypeError('content property must be given a tuple. This must be a tuple containing a ShellProgram instance and a list of Task objects, in that order.')
    
    def __init__(self, tsk_ls: list, prg: ShellProgram, aliases: dict = {}):
        if len(tsk_ls) <= 0:
            raise CfpUserInputError('Job objects must always contain at least one Task.')
        else:
            self.content = [prg, tsk_ls]
            self.aliases = aliases

    def add_task(self, tsk: Task):
        """This attaches the input task to the job"""
        if type(tsk) == Task:
            self.content[1].append(tsk)
        else:
            raise CfpTypeError('You can only add values of type Task to the task list')
    
    def tostring(self) -> str:
        try:
            progpath = str(self.content[0].fullpath)
            string = progpath + ' '
            for i in self.content[1]:
                string = string + i.tostring() + ' '
            return string.lstrip(' ').rstrip(' ')
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
    This class should be a relative of EVERY runner defined in the application. It defines only logic that must be present for all runners, and therefore lays out the minimal contract for this abstraction.

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

    #probably not needed
    # @property
    # def infile(self) -> Path:
    #     return self.__input_file

    # @infile.setter
    # def infile(self, arg: Union[str, PosixPath, WindowsPath]) -> None:
    #     if arg == None:
    #         pass
    #     elif type(arg) == str:
    #         self.__input_file = Path(arg)
    #     elif type(arg) == PosixPath or type(arg) == WindowsPath:
    #         self.__input_file = arg
        # else:
        #     raise CfpUserInputError('The value of infile must be a string representation of a file path or a pathlib.Path objict pointing to an actual file.')

    @property
    def infrom(self) -> InputHandler:
        """An InputHandler holding data bout the input to this runner"""
        return self.__in_from

    @infrom.setter
    def infrom(self, src: InputHandler) -> None:
        if issubclass(type(src), InputHandler):
            self.__in_from = src
        else:
            raise CfpTypeError('The infrom property must be set to None or to an InputHandler.')

    @property
    def outto(self) -> OutputHandler:
        """An OutputHandler holding data bout the output from this runner"""
        return self.__out_to
        

    @outto.setter
    def outto(self, dest) -> None:
        if issubclass(type(dest), OutputHandler):
            self.__out_to = dest
        else:
            raise CfpTypeError('The outto property can only contain values of type OutputHandler')

    @property
    def job(self) -> Job:
        """This is the job to be run with this runner"""
        return self.__cmd_list

    @job.setter
    def job(self, clist) -> None:
        if type(clist) == Job:
            self.__cmd_list = clist
        else:
            raise CfpTypeError('The job property can only contain values of type Job')
        
    @property
    def output(self):
        """This holds the output of a runner's last run. Before it is run for the first time, it is set to None"""
        return self.__output
    
    @output.setter
    def output(self, out):
        self.__output = out

    def __init__(self, job: Job, in_from: InputHandler=None, out_to: OutputHandler=None, infile: str=None, infile_type: FileType=FileType.CFP_INPUTFILE_TEXT_FMT_1):
        self.job = job
        self.outto = out_to
        if in_from != None and infile != None:
            raise CfpUserInputError("You cannot specify values for both input and infile")
        elif infile != None:
            pth = Path(infile)
            if Path.exists(pth):
                f = CfpFile(pth, infile_type)
                self.infrom = InputFileHandler([f], [])
                self.infile = pth
            else:
                raise CfpUserInputError("If included, value for infile must be a valid path")        
        elif in_from != None:
            if type(in_from) == InputHandler:
                self.infrom = in_from
                self.infile = None
        else:
            raise CfpUserInputError('you must give a value for either infile or in_from')
        

    def InitializeIOHandler(self, *handler_args, **handler_kwargs) -> IOHandlerBase:
        """
        This creates and returns an IOHandler with the input for this runner.
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

    def run():
        """This method must be overridden in all runners (in all child classes.) Here, it just passes."""
        pass

class CfpRunner(BaseRunner):
    """
    This is a highly dynamic class which is responsible for nearly all cfp runner types. If the init method is called directly, it will raise an error, but the various runner-type-getters, e.g. get_new_*_runner(), call init after setting a class property. After this is set, the runner will build itself according to its value.
    """
    # TODO: finish subprocess_runner
    
    DEFAULT_INPUT_SRC = 'subprocess.STDIN'
    DEFAULT_OUTPUT_SRC = 'subprocess.STDOUT'
    __r_type_old = ''

    @property
    def frompipe(self) -> bool:
        """Can be set to None or point to another runner which will be the input source for this one."""
        return self.__frompipe

    @frompipe.setter
    def frompipe(self, frm: bool) -> None:
        self.__frompipe = frm

    @property
    def topipe(self) -> bool:
        """Can be set to None or point to another runner which will be where the output to this runner is fed."""
        return self.__topipe

    @topipe.setter
    def topipe(self, to_pipe:bool) -> None:
        self.__topipe = to_pipe

    @property
    def runtype(self) -> RunType:
        """This defines the type of runner this is. Must be a value of type RunType."""
        return self.__invoc_type

    @runtype.setter
    def runtype(self, rt: RunType) -> bool:   
        self.__r_type = rt
       
    
    def __init__(self, runtype:RunType, job: Job, ih: InputHandler, oh: OutputHandler, topipe: BaseRunner=None, frompipe: BaseRunner=None):
        self.infrom = ih
        self.outto = oh
        self.job = job
        self.runtype = runtype     
        self.frompipe = frompipe
        self.topipe = topipe

    def configure(self):
        pass

    def __subprocrun_rnr_run_cmdstring(command_string: str) -> None:
        """This runs a command string with this runner."""
        try:
            subprocess.run(shlex.split(command_string), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
        except subprocess.SubprocessError:
            print('Something went wrong. Check input and "try" again.')

    def run(self, legacy: bool=False, frompipe: bool=False, topipe: bool=False):
        """This is how this runner runs its job"""
        try:
            if frompipe == False and topipe == False:
                if self.runtype == RunType.SUBPROCESS_RUN:
                    output = subprocess.run(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
                elif self.runtype == RunType.SUBPROCESS_RUN_LEGACY:
                    output = subprocess.call(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
                elif self.runtype == RunType.SUBPROCESS_POPEN:
                    output = subprocess.Popen(shlex.split(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE))
                elif self.runtype == RunType.SUBPROCESS_CHECKOUTPUT:
                    output = subprocess.check_output(shlex.split(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True))
                else:
                    raise CfpUserInputError('The runtype attribute is either not set or set to an invalid value. It must be of type RunType.')
                return output
            elif frompipe == True and topipe == True:
                if self.runtype == RunType.SUBPROCESS_RUN:
                    output = subprocess.run(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
                elif self.runtype == RunType.SUBPROCESS_RUN_LEGACY:
                    output = subprocess.call(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
                elif self.runtype == RunType.SUBPROCESS_POPEN:
                    output = subprocess.Popen(shlex.split(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE))
                elif self.runtype == RunType.SUBPROCESS_CHECKOUTPUT:
                    output = subprocess.check_output(shlex.split(self.job.tostring(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True))
                else:
                    raise CfpUserInputError('The runtype attribute is either not set or set to an invalid value. It must be of type RunType.')
                return output
        except Exception:
            raise CfpRuntimeError('Something went wrong while trying to run command.')

########                                                                                         ########
##########################################  ~~~~ CONTEXTS ~~~~  ##########################################
########                                                                                         ########

@dataclass
class Context:
    """
    This is the base class for all contexts. When subclassing this class, make sure that the new class a.) explicitly defines both __enter__ and __exit__ methods and b.) calls super.__enter__ and super.__exit__ from inside them.
    """
    # TODO:
        # Add __enter__() & __exit__() methods to each context subtype
            # if method doesnt finish due to crash, __exit__() needs to write a log entry into the .exceptilog file in the $CTX_DATA_DIR/log/ directory.
            # Both methods should come after __init__() at the end of the class.
                # If __init__() is not already the last method, move it.

    def __enter__(self):
        print('setting up environment')
        for i, (k, v) in enumerate(self.env_dict):
            j = i + 1
            print('adding var ' + j + ' of ' + len(self.env_dict))
            os.environ[k] = self.env_dict[k]
        else:
            print('finished setting up environment')

    def __exit__(self):
       for k in self.env_dict:
           del os.environ[k]   

    @property
    def namespace(self) -> str:
        """This will prefix every key in the environment dict. When the keys and values are loaded into the process environment, this is how you can tell the difference between the variables you've created and the ones that were already there."""
        return self.__name_space

    @namespace.setter
    def namespace(self, ns:str) -> None:
        self.__name_space = ns

    @property
    def ctx_type(self) -> str:
        """This describes the context. any time you create a subclass from this class, you will give your new class a ctx_type. For example, CfpShellContext has a ctx_type of 'shell_ctx'"""
        return self.__ctx_t

    @ctx_type.setter
    def ctx_type(self, ctxtype: str) -> None:
        self.__ctx_t = ctxtype 

    @property
    def env_dict(self) ->dict:
        """This contains all environment variables to be added to the process environment of the context. For any key-value-pair that is added, the key will be prfixed with the namespace followed by an underscore. This namespace helps to differentiate between the context variables and the variables that were already part of the process."""
        return self.__environ_dict

    @env_dict.setter
    def env_dict(self, ed: dict) -> None:
        self.__environ_dict = {}
        for k in ed:
            prefd = str(self.namespace) + '_' + str(k)
            self.__environ_dict[prefd] = ed[k]
                   
    def putenv(self,k: str, v: str) -> bool:
        """add a key-value-pair to the process environment. It will also be added to the env_dict property, as the two coincide"""
        prefd = str(self.namespace) + '_' + str(k)
        self.__environ_dict.update({prefd: v})
        os.environ[prefd] = v
        return True
            
    def getenv(self, key: str) -> str:
        """retrieve the value for a key in the env_dict property and in the process environment. The given key must be prefixed in the form 'self.namespace + _ + key'. For example if the namespace is 'hello' and the key is 'world', the new key will be 'hello_world'."""
        return self.__environ_dict[key]
    
    def print_info(self,outputFmt:str) -> None:
        """
        This prints some metadata about the current instance of the class, followed by a list of all current environment variables inside the namespace.
        TODO: make sure this is tested with a populated env_dict.
        """
        print.format('CURRENT CONTEXT:' )
        print.format('        Instance of Type:   {} Context', self.ctx_type)
        print.format('    Ctx Namespace Prefix:   {}_', self.namespace)
        print.format('    Ctx Inner Environment: {')
        for k,v in self.__environ_dict().items():
            if type(v) == str:
                print(f'              {k}: {v}')
            else:
                print(f'              {k}: {str(v)}') 

    def __init__(self):
        raise CfpInitializationError('Context is a base class that cannot be initialized. You must inherit from this class and initialize the subclass.')          

class CfpShellContext(Context):
    """
    This is a context for running commands in a shell such as bash or zsh. The shell process is run on top of a Python process with its own environment, with all variables prefixed with self.namespace, whose variables can be accessed in the same way as process envvars at context runtime.    
    """
    # TODO:

    shellpref_avail: bool = False

    def __enter__(self):
       super.__enter__()
   
    def __exit__(self):
      super.__exit__()    

    @property
    def shellchoice(self) -> str:
        """a string representing the user's preferred shell. Example 'bash' or 'zsh'. Note: This should be the exact program name of a shell program on the end user's system."""
        return self.__shell_choice

    @shellchoice.setter
    def shellchoice(self, choice: str) -> None: 
        if choice == None:
            raise CfpTypeError 
        self.__shell_choice = choice

    @property
    def current_shell(self) -> ShellProgram:
        """This contains a ShellProgram instance which usually points to the shellchoice shell. If that shell cant be found at runtime, it will default to either bash or cmd, depending on the operating system. Setting this will automatically update the runner with the new ShellProgram."""
        return self.__current_shell

    @current_shell.setter
    def current_shell(self, curr: ShellProgram) -> None:
        if issubclass(type(curr), ShellProgram):
            self.__current_shell = curr
            if self.current_shell != None:
                self.runner.job.content[0] = self.current_shell
        else:
            raise CfpTypeError('The value passed to current_shell must be of type ShellProgram')

    @property
    def runner(self) -> BaseRunner:
        """The context runner. This holds important info such as the shellprogram to be used and the commands to be run with that shell."""
        return self.__runner
    
    @runner.setter
    def runner(self, rnr):
        if issubclass(type(rnr), BaseRunner):
            self.__runner = rnr

        
    def __init__(self, env_dict: dict, runner: CfpRunner, shell_choice: str=None):
        """
        Init sets namespace, ctx_type and updates virtual_environment. Sets `cmds_fmt` to a 2d list where each outer element represents a command, itself represented by the inner list, with cmd[0] being the command and the rest of the inner list is its args. 
        """
        # super().__init__('shell_ctx','shell')
        self.namespace = 'SHELLCTX'
        self.ctx_type = 'shell_ctx'
        self.env_dict = env_dict
        self.runner = runner
        self.shellchoice = shell_choice
        self.current_shell = self.__get_a_shell(self.shellchoice)
        
    
    def __get_a_shell(self, shellpref:str):
        """
        This tries to return a ShellProgram instance with the fullpath set to self.shellpref. If the shellpref is not available in PATH on the runtime system, it tries to find bash or cmd in PATH. If neither of these are available, it returns None.".
        """
        sh_path = PathFinder.find_executable_fullpath(shellpref)
        if sh_path is not None:
            self.shellpref_avail = True
            sp = ShellProgram(shellpref, Path(sh_path), sp_opsys=str(os.name), sp_caller=str(os.getuid()))
            return sp
        if sh_path == None:
            self.shellpref_avail = False
            sh_path = PathFinder.find_executable_fullpath('bash')
            if sh_path != None:
                sp = ShellProgram(shellpref, Path(sh_path), sp_opsys=str(os.name), sp_caller=str(os.getuid()))
                return sp
            else:
                sh_path = PathFinder.find_executable_fullpath('cmd')
                if sh_path != None:
                    sp = ShellProgram(shellpref, Path(sh_path), sp_opsys=str(os.name), sp_caller=str(os.getuid()))
                    return sp
        return None

    def run_ctx(self, shellpath_clean):
        """This runs a job with the context runner."""
        self.__run_jobs_with_runner(self.job_runner, shellpath_clean)        
        
    def __run_jobs_with_runner(self, job_runner: CfpRunner, shellpath: str):
        """
        This runs a cmd using self.shellpref. self.shellpref_avail must be True. DO NOT SET IT YOURSELF! To set it, you must first run the check_for_preferred_shell() func above. If it is False, then the shell isn't installed on the current system. In this case 
        TODO: finish this method
                """
        job = self.runner.job


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
    This sets up the runner based on the value of ctx_type in the parent. Uses concept known as reflection in Java via running eval(runner_str) where runner str is based on ctx_type. This lets us dynamically build a string and then run that string as python3 code. e.g. say ctx_type is "subprocess". The resulting runner_str would be "subprocess.run(cmd)". 
    """
    # TODO:

    def __enter__(self):
       pass
   
    def __exit__(self):
       pass    
    
class CfpShellBasedTestContext(CfpShellContext):
    """
    Context for testing potential Codeforces solutions in a shell context
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
    def cf_lang_index(self) -> int:
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
    def lang(self) -> str:
        return self.__lang

    @lang.setter
    def lang(self,lng) -> None:
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
