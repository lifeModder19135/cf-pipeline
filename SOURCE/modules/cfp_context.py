import os, click, subprocess
from dataclasses import dataclass
from .cfp_errors import CfpInitializationError, CfpUserInputError
from enum import Enum
from shutil import which
from shlex import split, join
from pathlib import Path
from cfpipeline.SOURCE.lib.libcfp_metautils import *

#          ^
#          ^
#          ^
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
#  Keys  Values    corque  Input   |     Job  
#                  board   |   Output    | |
#                (queue)   |    |       |   |
#                          |   |       |     |
#                        Message    Shell    CmdMode
#                                            |    |
#                                            |     |
#                                            |      |
#                                      cmdModule  {[cmdmodule.Follower], ...} 
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
#     
#
# 
#
# 
#
# 
#

########                                                                                         ########
##########################################  ~~~~ CONTEXTS ~~~~  ##########################################
########                                                                                         ########

@dataclass
class Context:
    """
    Base for all contexts. 
    """
    namespace: str 
    ctx_type: str 
    env_dict: dict
                   
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
    pass
    
class CfpShellBasedTestContext(CfpShellContext):

    cf_allowedlangs = ['C# mono',
                        'D DMD32',
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
    
    runner: CfpRunner = None
    
    # represents the chosen language's index in the cf_allowedlangs list 
    cf_lang_index = -1 

    def __init__(self, cmds, rnnr: CpfRunner, shell_env: str, language: str, **envvars: any):
        super().__init__(cmds, rnnr,  envvars)
        self.setlang(language)
    
    def setlang(self):
        for i,lang_choice in enumerate(self.cf_allowedlangs):
            if lang_choice.lower() in ''.join(list(map(str, language.split(' ')))).lower():
                self.cf_lang_index = i
        if cf_lang_index < 0:
            raise IOError('You must provide a language!')
        else:    
            lang = self.cf_allowedlangs[cf_lang_index]
            self.putenv('solutionlanguage', lang)
            
########                                                                                         ########
##########################################  ~~~~ RUNNERS ~~~~  ##########################################
########                                                                                         ########
            
class CfpRunner:
    """
    This is a highly dynamic class which is responsible for nearly all cfp runner types. If the init method 
    is called directly, it will raise an error, but the various runner-type-getters, e.g. get_new_*_runner(), call init after setting a class property. After this is set, the runner will build itself according to its value.
    
    TODO:
    """
    
    runtype = None
    frompipe: bool = False
    topipe: bool = False
    default_input_src = subprocess.STDIN, 
    default_output_src = subprocess.STDOUT
    argstring: Argstring = ''
    
    def __init__(self):
        if self.runtype is None:
            raise CfpInitializationError("You cannot invoke this __init__() method directly. Try using one of the @classmethods defined by this class to get a new instance.")
        elif self.runtype == Runtype.SUBPROCESS:
            self.frompipe = False
            self.topipe = False
        elif self.runtype == Runtype.SUBPROCESS_LEGACY:
            self.strategy = 'subprocess.'      
            
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
        
    def __setRuntype(self, rt: Runtype):
        self.runtype = rt
        return True


    def __subprocrun_rnr_run_cmdstring(command_string, ):
        try:
            subprocess.run(command_string,)
        except subprocess.SubprocessError:
            print('Something went wrong. Check input and "try" again.')
    

    

    
class Command_Line:
    cl_aliases: list[str] = None
    content: List[Command_String] = None
    
    def __init__(self, cmd_ls: list[Command_String], *aliases):
        if len(cmd_ls) <= 0:
            raise CfpUserInputError('Command_Line objects must always contain at least one Command_string.')
        else:
            self.content = cmd_ls
    
    def to_string(self):
        pass
        
    
    
    
@dataclass
class CfpFile:
    """
    Base class for Executable, Source_File, Shell_Application, Input_File, and anything with a location: Path attribute. Not all will be eligible for File.open(), as directories are files as well.  
    """    
    
    location: Path = None
    size_in_bytes: int = None
    isOpenable: bool = None

class Argstring(str):
    def to_cmd_objs(self):
        pass 

########                                                                                         ########
###########################################  ~~~~ ENUMS ~~~~  ###########################################
########                                                                                         ########

class Runtype(Enum):
    """
    Args:
        Enum ([type]): [description]
    """
    # 'asynchronous single-command runner using subprocess api'
    SUBPROCESS = {typevalue_string: 'subprocess_solo', 
                  topipe: False, 
                  frompipe: False, 
                  default_input_src: subprocess.STDIN, 
                  default_output_src: subprocess.STDOUT}
    # 'asynchronous pipe-exit command runner using subprocess api'
    SUBPROCESS_LEGACY = {description_string: 'subprocess_legacy', 
                         exec_string: 'subprocess.call().out'}    
    
class ResultResolutionMode(Enum):
    """
    This is meant to be a parameter for functions that configure one or more values that are persisted in the application after the function call finishes. It lets the caller specify how they want that value to be set /given. For example, the function could pass the value to its caller via return stmt, set a class variable, add a kv pair to env_dict, etc. To use, just add a kwarg of `arg: ResultResolutionMode = XXX` to func, where XXXX (the default) is one of the options below.
    """
    # Resolver should return result in the func return statement.
    RETURN_STATEMENT = 1
    INSTANCE_PROPERTY = 2
    ENV_DICT = "self.putenv({},{})"
    