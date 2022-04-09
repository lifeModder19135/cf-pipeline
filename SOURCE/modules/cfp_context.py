import os, click, invoke, subprocess, fileinput, shutil
import sys
from types import NoneType
from dataclasses import dataclass

from matplotlib.pyplot import close
from .cfp_errors import CfpInitializationError, CfpNotExecutableError, CfpPermissionDeniedError, CfpRuntimeError, CfpTimeoutError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpValueError
from enum import Enum
# from shutil import which
from shlex import split, join, whitespace_split
from pathlib import Path
from ..lib import libcfapi_utils

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
#*         of specifiers and nested sections a.k.a. subsections. 
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

class InputType(Enum):
    """
    properties:
        Enum ([type]): [description]
    """
    # TODO:

    INFILE = 0
    INSTREAM = 1
    INPIPE = 2

class OutputType(Enum):
    """
    properties:
        Enum ([type]): [description]
    """
    # TODO:

    OUTFILE = 3
    OUTSTREAM = 4
    OUTPIPE = 5

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
    CFP_INPUTFILE_FMT_1 = 3
    CFP_INPUTFILE_FMT_2 = 4
    CFP_OUTPUTFILE = 5
    CFP_DIFF_FILE = 6
    SOURCE_FILE_GENERIC = 7
    SOURCE_FILE_PY2 = 8
    SOURCE_FILE_PY3 = 9
    SOURCE_FILE_C = 10
    SOURCE_FILE_CPP = 11
    SOURCE_FILE_JAVA = 12
    DIRECTORY = 13


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

########                                                                                         ########
########################################  ~~~~ IO_HANDLERS ~~~~  ########################################
########                                                                                         ########    

class IOHandlerBase:
    """
    properties:
        [type]: [description]
    """
    # TODO:

    handler_args = []
    
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            for a in args:
                self.handler_args.append(str(a))
            for k,v in kwargs:
                st = f'{k}={v}'
                self.handler_args.append(st)
        return self
    
    
    def set_io_type(self, io_type: str):
        """
        io_type is either input or output, otherwise throw error.
        """
        if io_type == 'i' or io_type == 'in' or io_type == 'input':    
            self.io_type = 'I'
        elif io_type == 'o' or io_type == 'out' or io_type == 'output':
            self.io_type = 'O'
        else:
            raise CfpUserInputError(f'Invalid value given for parameter {io_type}')
        return True
    
    @property
    def io_type(self)->IOType:
        return self.__io_t

    @io_type.setter
    def io_type(self, iotype: IOType)->None:
        self.__io_t = iotype

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
    def __init__(self, itype, *args, file, **kwargs):
        super().__init__( itype, *args, file=file, **kwargs)

class OutputHandler(IOHandlerBase):
    """
    Description: Active container which implements an interface for controlling what happens to, and what is affected by, the output of a runner in a context.
    """
    # TODO:
    #   - add implementation

    pass
    

########                                                                                         ########
########################################  ~~~~ RUNNER SUBS ~~~~  ########################################
########                                                                                         ########     

class InputCommandString(str):
    """
    description: represents a string containing one or more shell commands
    properties:
        shell_lang: see method docstring
    """
    # TODO:
    
    @property
    def shell_lang(self):
        """
        Description: This is the shell that this object's shellscript code should be evaluated with
        Returns: The shell_lang property's current value
        Defaults to: Bash 
        """
        if not self.__flavor:
            self.__flavor = 'Bash'
        return self.__flavor
    
    @shell_lang.setter
    def shell_lang(self,sh):
        self.__flavor = sh

    def to_cmd_objs(self):
        """
        Description: This method converts the method to a list of Command objects 
        """
        pass 

class Program(Path):
    """
    Description: Represents a computer program
    properties: None
    """
    # TODO:
    
    @property
    def operating_system(self) -> str:
        return self.__op_sys
    
    
    @operating_system.setter
    def operating_system(self, o_s:str=None) -> None:
        if o_s is None:
            self.__op_sys = sys.platform
        else:
            self.__op_sys = o_s
    
    @property
    def invoked_by(self):
        return self.__caller
    
    @invoked_by.setter
    def invoked_by(self, user:str=None):
        if user is None:
            self.__caller = os.path.expandvars('$USER')
        elif type(user) == str:
            self.__caller = user
        else:
            raise CfpTypeError()
            
    @property
    def fullpath(self) -> str:
        return self.__full_path
    
    @fullpath.setter
    def fullpath(self, val:str) -> None:
        self.__full_path = val

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

    def __init__(input_src):
        super().__init__(input_src)

class CmdArgstring(str):    
    """
    properties:
        [type]: [description]
    """
    # TODO:

    def __init__(input):
        super().__init__(input)

class CmdArglist(str):
    """
    properties:
        [type]: [description]
    """
    # TODO:

    def __init__(input_src):
        super().__init__(input_src)

class Command:
    """
    properties:
        [type]: [description]
    """
    # TODO:

    exe: str = None
    args: list = None
    
    def __init__(self):
        pass

@dataclass
class CfpFile:
    """
    Base class for Executable, Source_File, Shell_Application, Input_File, and anything with a location: Path attribute. Not all will be eligible for File.open(), as directories are files as well.  
    """    
    # TODO:

    handler:IOHandlerBase
    location: Path = None
    filetype: str = None
    size_in_bytes: int = None
    isOpenable: bool = None
    

    @property
    def filetype(self):
        """
        explicit params: n/a
        input: self
        output: string - file type of self
        """
        return self.__f_type

    @filetype.setter
    def filetype(self, filetype):
        self.__f_type = filetype

    @property
    def getContent(self):
        if self.__f_type() == 'unknown':
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
        self.__content = tup  
    
    def __init__(self, cmd_ls: "list[Task]", *aliases):
        if len(cmd_ls) <= 0:
            raise CfpUserInputError('Command_Line objects must always contain at least one Command_string.')
        else:
            self.content = cmd_ls
    
    def to_string(self):
        pass

########                                                                                         ########
##########################################  ~~~~ RUNNERS ~~~~  ##########################################
########                                                                                         ########

@dataclass
class BaseRunner:
    """
    Description: This class should be a relative of EVERY runner defined in the application. It defines only logic that must be present for all runners, and therefore lays out the minimal contract for this abstraction.
    Properties:
        infile->pathlib.Path of the input file for this runner

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
    def infrom(self, arg)->None:
        self.__in_from = arg

    @property
    def outto(self)-> OutputHandler:
        if type(self.__out_to) == OutputHandler:
            return self.__out_to
        else:
            raise TypeError

    @outto.setter
    def outto(self, dest)->None:
        self.__out_to = dest

    @property
    def job(self, arg)->None:
        return self.__cmd_list

    @job.setter
    def job(self, clist)->None:
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
             
    def InitializeIOHandler(self, **handler_args):
        """
        Description: creates and returns an IOHandler with 
        Args: [
            handler_args: 
        ]
        Raises: [
            CfpUserInputError : [Raised if the data given to the instance is invalid]
            IOError: [Called as a parent of the first Error]
            CfpInitializationError: [Raised if a system error is caught upon init of the link]
        ]
        Returns:
            IOHandler: [This class is responsible for the IO of its Runner. May be InputIOHandler or OutputIOHandler]
        """
        if self.infile:
            handler = IOHandlerBase(handler_args)
        return handler

class CfpRunner(BaseRunner):
    """
    This is a highly dynamic class which is responsible for nearly all cfp runner types. If the init method 
    is called directly, it will raise an error, but the various runner-type-getters, e.g. get_new_*_runner(), call init after setting a class property. After this is set, the runner will build itself according to its value.
    """
    # TODO:
    
    DEFAULT_INPUT_SRC = 'subprocess.STDIN'
    DEFAULT_OUTPUT_SRC = 'subprocess.STDOUT'
    runtype = None
    frompipe: bool = False
    topipe: bool = False
    argstring: str = ''
    
    def __init__(self):
        if self.runtype is None:
            raise CfpInitializationError("You cannot invoke this __init__() method directly. Try using one of the @classmethods defined by this class to get a new instance.")
        elif self.runtype == RunType.SUBPROCESS:
            self.frompipe = False
            self.topipe = False
        elif self.runtype == RunType.SUBPROCESS_LEGACY:
            self.strategy = 'subprocess_check_output'      
            
    def configure(self):
        pass
    
    def get_new_subprocess_runner(self, legacy:bool=False):
        """
        What it says. It returns a fresh instance of CfpRunner with the Runtype set to SUBPROCESS.   
        """
        if legacy == True:
            self.setRuntype(RunType.SUBPROCESS_LEGACY)
        else:
            self.setRuntype(RunType.SUBPROCESS)             
        self.__init__()

    @property
    def runtype(self)->RunType:
        return self.__invoc_type

    @runtype.setter
    def runtype(self, rt: RunType)->bool:
        try:
            if self.__invoc_type and self.__invoc_type is not None:
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
        TODO: make sure this is tested with a populated env_dict. Need to create a 
        """
        print.format('CURRENT CONTEXT:' )
        print.format('        Instance of Type:   {} Context', self.ctx_type)
        print.format('    Ctx Namespace Prefix:   {}_')
        print.format('   Ctx Inner Environment: \{')
        for k,v in self.env_dict().items():
            if type(v) == str:
                print(f'              {k}: {v}')
            else:
                print(f'              {k}: {str(v)}')           

class CfpShellContext(Context):
    """
    This is a context for running commands in a shell such as bash or zsh. The bash process is run on top of a Python process with its own environment that is kept seperate from the process environment by default, but whose variables can be accessed in the same way as process envvars at context runtime.    """
    # TODO:


    @property
    def shellchoice(self) -> str:
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

    @property
    def cmds(self) -> list:
        return self.__cmd_list
        
    def __init__(self, cmds, runner: CfpRunner, shell_env: str, **envvars):
        """
        Init calls parent init (sets namespace, ctx_type) and updates virtual_environment. Sets `cmds_fmt` to a 2d list where each outer element represents a command, itself represented by the inner list, with cmd[0] being the command and the rest of the inner list is its args. 
        """
        super().__init__('shell_ctx','shell')
        
        self.env_dict.update(envvars)
        self.shellpath = self.check_for_preferred_shell(self.shellchoice, resolve_mode="returnstatement")
    
    def check_for_preferred_shell(self, shellpref:str):
        """
        runs which command with shellname as argument. If cmd returns empty, self.shellpref_avail is set to False and this func returns False. otherwise,it is set to True, and func returns the path which the os uses to execute it, usually "$PREFIX/bin/shellname".
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
        simply runs cmd using self.shellpref. self.shellpref_avail must be True. DO NOT SET IT YOURSELF! To set it, you must first run the check_for_preferred_shell() func above. If it is False, then the shell isn't installed on the current system. In this case 
        """
        pass       

    def __prep_commands_list(self, cmd_list:"list[str]", shellpath):
        self.cmds_fmt = list()
        for c_str in cmd_list:
            for cmd in c_str:
                if type(cmd) == list:
                    self.cmds_fmt.append(cmd)
                elif type(cmd) == str:
                    self.cmds_fmt.append(whitespace_split(cmd))   

    def __prep_commands_str(self, cmd_str:str, shellpath):
        cmds_ls = cmd_str.split('&&')
        self.__prep_commands_list(cmds_ls,shellpath)
                
class DynamicStrRunnerContext(Context): 
    """
    Sets up the runner based on the value of ctx_type in the parent. Uses concept known as reflection in Java via running eval(runner_str) where runner str is based on ctx_type. This lets us dynamically build a string and then run that string as python3 code. e.g. say ctx_type is "subprocess". The resulting runner_str would be "subprocess.run(cmd)". 
    """
    # TODO:

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
        if type(self.__cfp_runner) is NoneType:
            return None
        elif type(self.__cfp_runner) is CfpRunner:
            return self.__cfp_runner
        else:
            raise TypeError

    @solutions_testrunner.setter
    def solutions_testrunner(self, rnr): 
        self.__cfp_runner = rnr
    
    # represents the chosen language's index in the cf_allowedlangs list 
    cf_lang_index = -1

    @property
    def lang(self)->str:
        return self.__lang

    @lang.setter
    def lang(self,lng)->None:
        self.__lang = lng
        return None

    def setlang(self, language:LanguageChoice) :
        """
        Believe it or not, this one sets the lang
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


