import os, click



#          ^
#          ^
#          ^
#          |
#  has-a = |   /  is-a =  < < < ----

#                 context < < < ----------------------------  test_contest
#                  |   |
#                 |     |
#                |       |
#               |         |
#              |           |
#        environment     
#    
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#


@dataclass
class Context:
    '''
    Base for all contexts. 
    '''
    namespace: str = ''
    ctx_type: str = ''
    


     

class Cfp_Shell_Context(Context):
    '''
    This is a context for running commands in a shell such as bash or zsh. The bash process is run on top of a Python process with its own environment that is kept seperate from the process environment by default, but whose variables can be accessed in the same way as process envvars at context runtime.
    '''
    env_dict = dict()
    shell = ''
    cmds:list[Command] = []
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
                        'JavaScriptV8'
                        'nodejs'
                       ]
    # represents the chosen language's index in the cf_allowedlangs list 
    cf_lang_index = -1   
    
    def __init__(self, cmds, **envvars):
        '''
        Init calls parent init (sets namespace, ctx_type) and updates virtual_environment 
        '''
        super().__init__('shell_ctx','shell')
        
        self.env_dict.update(envvars)
        if type(cmds) == list:
            if type(cmds[0]) == list:
                pass
        elif type(cmds) == str:
            pass
            
    def putenv(k, v):
        env_dict.update({k: v})
        return True
    
    def setlang(self):
        if cf_lang_index < 0:
            raise IOError('You must provide a language!')
        else:
            lang = self.cf_allowedlangs[cf_lang_index]
            self.putenv('solutionlanguage', lang)
            
    def getenv(self, key):
        return self.env_dict[key]
    
    def check_for_preferred_shell(self, shellpref:string):
        '''runs which command with shellname as argument. If cmd returns empty, self.shellpref_avail is set to False and this func returns False. otherwise,it is set to True, and func returns the path which the os uses to execute it, usually "$PREFIX/bin/shellname".'''
        
    
    def __run_commands(self,cmd: str, shellpath):
        '''simply runs cmd using self.shellpref. self.shellpref_avail must be True. DO NOT SET IT YOURSELF! To set it, you must first run the check_for_preferred_shell() func above. If it is False, then the shell isn't installed on the current system. In this case '''
        cmds_ls = cmds.split('&&')
        for c in cmds_ls:
            pass
            
                
class DynamicStrRunnerContext(Context): 
    '''sets up the runner based on the value of ctx_type in the parent. Uses concept known as reflection in Java via running eval(runner_str) where runner str is based on ctx_type. This lets us dynamically build a string and then run that string as python3 code. e.g. say ctx_type is "subprocess". The resulting runner_str would be "subprocess.run(cmd)". '''
    
class CfpTestContext(CfpContext):


    def __init__(self, **envvars):
        super().__init__(envvars)
         