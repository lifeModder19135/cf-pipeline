import os



#          ^
#          ^
#          ^
#          |
#  has-a = |   /  is-a =  ---- > > >

#                 context ---------------------------- > > >  test_contest
#                  |   |
#                 |     |
#                |       |
#               |         |
#              |           |
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
#     

class CfpContext:
    '''
    This is a context which is run on top of a process with its own environment that is kept seperate from the process environment by default, but whose variables can be accessed in the same way as process envvars at context runtime.
    '''
    env_dict = dict()
    progs = []
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
    cf_lang_index = -1   
    
    def __init__(self, cmds, **envvars):
        '''
        
        '''
        env_dict.update(envvars)
        if type(cmds) == list:
            if type(cmds[0]) == list:
        elif type(cmds) == str:
            cmds_ls = cmds.split('|')
            for c in cmds_ls:
                c.
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
    
    
    
class CfpTestContext(CfpContext):


    def __init__(self, **envvars):
        super().__init__(envvars)
         