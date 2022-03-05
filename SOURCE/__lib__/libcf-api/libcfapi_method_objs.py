

import click
from enum import Enum
import string

class ParamTypes(Enum):
    STRING = 0
    INT = 1
    FLOAT = 2
    DOUBLE = 3
    BYTE = 4
    LIST = 5
    TUPLE = 6
    SET = 7
    DICT = 8
    OBJECT_SUBTYPE = 9

class Apis(Enum):
    CODEFORCES = 'codeforces.com'

class CodeforcesApiMethodValues(Enum):
    '''
    A comprehensive listing of all Codeforces api Methods supported by the program at a time.
    '''
    BLOGENTRY_COMMENTS = 'blogEntry.comments'
    BLOGENTRY_VIEW = 'blogEntry.view'
    CONTEST_HACKS = 'contest.hacks'
    CONTEST_LIST = 'contest.list'
    CONTEST_RATINGCHANGES = 'contest.ratingChanges'
    CONTEST_STANDINGS = 'contest.standings'
    CONTEST_STATUS = 'contest.status'
    PROBLEMSET_PROBLEMS = 'problemset.problems'
    PROBLEMSET_RECENTSTATUS = 'problemset.recentStatus'
    RECENTACTIONS = 'recentActions'
    USER_BLOGENTRIES = 'user.blogEntries'
    USER_FRIENDS = 'user.friends'
    USER_INFO = 'user.info'
    USER_RATEDLIST = 'user.ratedList'
    USER_RATING = 'user.rating'
    USER_STATUS = 'user.status'
    
    
    
class ParamType(click.ParamType):

    def check_typehint(typehint:str)->ParamTypes:
        x = typehint.lower() 
        res:ParamTypes = None
        if x == 'str' or x == 'string':
            res = ParamTypes.STRING
        elif x == 'int' or x == 'integer':
            res = ParamTypes.INT
        elif x == 'float' or x == 'floating_point' or x == 'floating point' or x == 'floating-point':
            res = ParamTypes.FLOAT
        elif x == 'double':
            res = ParamTypes.DOUBLE
        elif x == 'byte':
            res = ParamTypes.BYTE
        elif x == 'list':
            res = ParamTypes.LIST
        elif x == 'tuple':
            res = ParamTypes.TUPLE
        elif x == 'set':
            res = ParamTypes.SET
        elif x == 'dict ' or x == 'dictionary':
            res = ParamTypes.DICT
        elif x == 'object' or x == 'obj' or x == 'object_subtype':
            res = ParamTypes.OBJECT_SUBTYPE
        else:
            raise ValueError('Type not directly supported. If you feel there has been a mistake, and you are SURE that the api is expecting the type you've provided, then try running the as_value() method instead')
        return res
    
        
    
    def set_type(typehint:str=None):
        if typehint is not None:
            self.type = self.check_type(typehint)
    def __init__(self):
        self
        pass

class APIMethodParameter(object):
    '''
    This is the class used to define a parameter for an api method. When a method object is defined, any parameters that this method takes will be declared as type api_method_parameter. It does not hold the value, it just checks that the value passes all of the specified constraints. 
    '''
    name: string = None
    require: bool = None
    type: ParamType = None
    default_value = None 
    
    def __init__(self, def_val:Any=None, required:bool=False, param_type:ParameterType='obj', types_accepted:dictionary=None):
        '''
        params:
            default_value:
                the value to which the parameter will be set if no value arg is given. 
            required:
                whether or not to fail if the parameter is not given.
            types_accepted: 
                a dict specifying the types in which the parameter value(s) can be given. For any types accepted, a function must be provided to convert that type to the type needed.
            parameter_type
                
            typehint set to obj as a catchall, as every type in python3 is a subtype of object (except object, which also works.) 
        '''
        self.require = required
        self.default_value = def_val
        self.parameter_type = param_type
        self.types_accepted = types_accepted
        if len(types_accepted) == 1:
            if self.parameter_type == self.types_accepted:
            if 
            
class ReturnType(json.JSONEncoder):
    '''
    Return type of an ApiMethod object.
    '''
    class ReturnObject(object):
        pass

    def __init__(self,input):
        super.__init__()    
            
class ApiMethod(object):
    '''
    A callable api method specified in an api. 
    '''
    @property
    def parentapi(self):
        '''
        For now it is hard-wired as Codeforces. Eventually, platform will support other comp. coding apis.
        This property is only in place for that eventuality, at which time the value will be added as a configuration option. The getter and setter defined here will obviously need altered as well. 
        '''
        return 'codeforces.com/api/'
    
    @parent_api.setter
    def setparentapi(self, arg):
        self._api_string = arg
        return True

    @property
    def conn_protocol(self):
        return self._c_proto

    @conn_protocol.setter
    def conn_protocol(self, arg):
        self._c_proto = arg

    @property
    def params_list(self):
        return self._p_list

    @params_list.setter
    def params_list(self, args):
        '''
        sets parameters for an a
        '''
        self._p_list = {}
        if len(args[1:-1]) == 0
            pass
        elif len(args[1:-1]) == 1
            if type(args) == 'dict':
                for k,v in args:
                    self._p_list[str(k)] = v
            elif type(args) == 'list' and (len(args[1]) % 2) == 0:
                # list w/ even amt of items. Set to params_list as 'k,v,k,v,k,v....'
                keys = []
                vals = []
                for i in args[1]:
                    if type(i) != 'str':
                        print('The `params_list` setter only supports input in the format of a dictionary or a list of strings representing kevs and values in k,v,k,v,k,v.. order. {} is not a string')
                        return False
                    elif len(keys) > len(vals):
                        vals.append(i)
                    else:
                        keys.append(i)
                if len(keys) == len(vals) and len(keys) == (len(args[1]) / 2):
                    for i in range(len(keys)):
                    _p_list[keys[i]] = vals[i]
        else: 
            raise ValueError

        return self._p_list 

    @property
    def call_string(self):
        return self._cs     
        
    @call_string.setter
    def call_string(self, arg):
        self._cs = arg

    def run_query():
        pass
    
    def __init__(self,*params:ApiMethodParameters)->ParamTypes:
        pass

    def is_member_of(self, api)


class CodeforcesApiMethod(ApiMethod):
    
    @property
    def parentapi(self):
        '''
        For now it is hard-wired as Codeforces. Eventually, platform will support other comp. coding apis.
        This property is only in place for that eventuality, at which time the value will be added as a configuration option. The getter and setter defined here will obviously need altered as well. 
        '''
        return 'codeforces.com/api/'
    
    @parent_api.setter
    def setparentapi(self, *args):
        click.echo('The current version of this program only supports codeforces.com. The `parent_api` property and it's methods are only included to make provisions for future versions.')
        return False

    @property
    def conn_protocol(self):
        return self._c_proto

    @property
    def call_string(self):
        self._cs =     
        
    def run_query():
        pass
    
    def __init__(self,*params:ApiMethodParameters)->ParamTypes:
        pass
    