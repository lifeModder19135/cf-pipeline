import os, click, invoke, subprocess
from types import NoneType
from dataclasses import dataclass
from .cfp_errors import CfpInitializationError, CfpUserInputError
from enum import Enum
from shutil import which
from shlex import split, join
from pathlib import Path
from ..__lib__.libcfp_metautils import *

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
        Enum ([type]): [description]
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
    This is meant to be a parameter for functions that configure one or more values that are persisted in the application after the function call finishes. It lets the caller specify how they want that value to be set /given. For example, the function could pass the value to its caller via return stmt, set a class variable, add a kv pair to env_dict, etc. To use, just add a kwarg of `arg: ResultResolutionMode = XXX` to func, where XXXX (the default) is one of the options below.
    """
    # TODO:

    # Resolver should return result in the func return statement.
    RETURN_STATEMENT = "return {}".format(args[2])
    INSTANCE_PROPERTY = "{}({})".format(args[2], args[3])
    ENV_DICT = "self.putenv({},{})".format(args[2], args[3])

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

    PLAINTEXT_FILE = 0
    INTS_ONLY_TEXT_FILE = 1
    # For more info about FILE_FMT_N, see section 'IO File Formats' at the top of this module
    CFP_INPUTFILE_FMT_1 = 2
    CFP_INPUTFILE_FMT_2 = 3
    SOURCE_FILE_GENERIC = 4
    SOURCE_FILE_PY2 = 5
    SOURCE_FILE_PY3 = 6
    SOURCE_FILE_C = 7
    SOURCE_FILE_CPP = 8


class LanguageChoice(Enum):
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
########################################  ~~~~ RUNNER SUBS ~~~~  ########################################
########                                                                                         ########     

class InputCommandString(str):
    """
    properties:
        [type]: [description]
    """
    # TODO:

    def to_cmd_objs(self):
        pass 

class Program(Path):
    """
    properties:
        [type]: [description]
    """
    # TODO:

    def __init__(input_src):
        super().__init__(input_src)

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
        if self.get_filetype() == 'unknown':
            
        
    def from_scratch(self, header):
        pass
        

class Task:
    """
    Represents a group of one or more commands connected together via pipes / fifos. IMPORTANT: commands which are connected via `&&` , `||` , or `;` are not 
    """
    # TODO:

    content:list[Command] = None
    
    def __init__(self):
        pass

class Job:
    """
    Params:
            top_level -- constant -- boolean -- if true, this Job is meant for running lower level jobs. If false, it is a lower_level itself, and is for running Task lists
    """
    # TODO:

    TOP_LEVEL:bool = False
    aliases: list[str] = None
    content: list[Task] = None
    
    def __init__(self, cmd_ls: list[Task], *aliases):
        if len(cmd_ls) <= 0:
            raise CfpUserInputError('Command_Line objects must always contain at least one Command_string.')
        else:
            self.content = cmd_ls
    
    def to_string(self):
        pass
              
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
        self.infrom = in_from 
        self.outto = out_to
        self.infile = infile
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
            handler = IOHandler(handler_args)
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
    argstring: Argstring = ''
    
    def __init__(self):
        if self.runtype is None:
            raise CfpInitializationError("You cannot invoke this __init__() method directly. Try using one of the @classmethods defined by this class to get a new instance.")
        elif self.runtype == Runtype.SUBPROCESS:
            self.frompipe = False
            self.topipe = False
        elif self.runtype == Runtype.SUBPROCESS_LEGACY:
            self.strategy = 'subprocess_check_output'      
            
    def configure(self):
        pass
    
    def get_new_subprocess_runner(self, legacy:bool=False):
        """
        What it says. It returns a fresh instance of CfpRunner with the Runtype set to SUBPROCESS.   
        """
        if legacy == True:
            self.setRuntype(Runtype.SUBPROCESS_LEGACY)
        else:
            self.setRuntype(Runtype.SUBPROCESS)             
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
    Base for all contexts.
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
        return self.__ctx_t: str 

    @ctx_type.setter
    def ctx_type(self, ctxtype: str)->None:
        self.__ctx_t = ctxtype 

    @property
    def env_dict(self)->dict:
        return self.__environ_dict

    @env_dict.setter
    def env_dict(self, ed: dict):
        if len(self.__environ_dict) == 0
            self.__environ_dict = 
        self.__environ_dict
                   
    def putenv(k, v):
        env_dict.update({k: v})
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
        for k,v in env_dict.items():
            if type(v) == string:
                print(f'              {k}: {v}')
            else:
                print(f'              {k}: {str(v)}')           

class CfpShellContext(Context):
    '''
    This is a context for running commands in a shell such as bash or zsh. The bash process is run on top of a Python process with its own environment that is kept seperate from the process environment by default, but whose variables can be accessed in the same way as process envvars at context runtime.
    '''
    # TODO:

    shellchoice: str = ''
    cmds: list = []
        
    def __init__(self, cmds, runner: CfpRunner, shell_env: str, **envvars):
        '''
        Init calls parent init (sets namespace, ctx_type) and updates virtual_environment. Sets `cmds_fmt` to a 2d list where each outer element represents a command, itself represented by the inner list, with cmd[0] being the command and the rest of the inner list is its args. 
        '''
        super().__init__('shell_ctx','shell')
        
        self.env_dict.update(envvars)
        self.shellpath = check_for_preferred_shell(self.shellchoice, resolve_mode="returnstatement")
    
    def check_for_preferred_shell(self, shellpref:str):
        '''runs which command with shellname as argument. If cmd returns empty, self.shellpref_avail is set to False and this func returns False. otherwise,it is set to True, and func returns the path which the os uses to execute it, usually "$PREFIX/bin/shellname".'''
        sh_path = shutil.which(shellpref)
        if sh_path is not None:
            return Path(sh_path)
        else:
            return False

    def run_ctx(self):
        self.__run_jobs_with_runner(self.job_runner, shellpath_clean)        
        
    def __run_jobs_with_runner(self, job_runner: CfpRunner, shellpath: str):
        '''simply runs cmd using self.shellpref. self.shellpref_avail must be True. DO NOT SET IT YOURSELF! To set it, you must first run the check_for_preferred_shell() func above. If it is False, then the shell isn't installed on the current system. In this case '''
        pass       
        
    def __prep_commands(self, cmd_str: list[str], shellpath):
        cmds_ls = command.split('&&')
        self.cmds_fmt = list()
        for c_str in cmds_ls:
            for cmd in c_str:
                if type(cmd) == list:
                    self.cmds_fmt.append(cmd)
                elif type(cmd) == str:
                    self.cmds_fmt.append(shlex.whitespace_split(cmd))            
                
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

    def setlang(self, language:) :
        '''

        '''
        for i,lang_option in enumerate(self.cf_allowedlangs):
            if lang_option.lower() in '_'.join(list(map(str, language.split(' ')))).lower():
                self.cf_lang_index = i
                break
        elif self.default_lang
        if cf_lang_index < 0:
            raise IOError('You must provide a language!')
        else:    
            lang = self.cf_allowedlangs[cf_lang_index]
            self.putenv('solutionlanguage', lang)

    def __init__(self, cmds, rnnr: CfpRunner, shell_env: str, language: str, **envvars: any):
        super().__init__(cmds, rnnr,  envvars)
        self.setlang(language)


