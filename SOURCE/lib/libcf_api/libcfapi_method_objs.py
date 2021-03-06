
import click, json
from enum import Enum
from .libcfapi_utils import formatfuncstr
from SOURCE.modules import cfp_errors


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
    RESOLVE = 99

class CpApiTuples(Enum):
    """
    Description: Enum hybrid class that exposes an interface to the various "A-list" competitive progrsmming sites, via their apis if available, and if not, via any means necessary. 
    Value:
        Type: tuple[4]
        Members:
            ID:  str-wrapped 2-digit int -- wrapped to include leading zeroes.
            UrlBase: list of strings -- includes the subdomain and domain of url -- must be a list for the parser, even if it is only 1 item.
            SiteTypeExtension: int between 0 & 4 -- 0-'com' 1-'org' 2-'io' 3-'edu' 4-'net' -- 0 will usually do the trick.
            Relpath: string or string-like -- path from the api site index to the api's base -- i.e. everything after (and including) the first '/' in api url.
            RequestType: GET, POST, PUT, DELETE --The type of http request that the endpoint expects.
            RequestArgs: 
                Description: Dict[argname: argvalue] -- any arguments specific to a certain type of request. Must be kwargs as the surrounding type is dict. If none are needed, just include an empty dictionary '{}' for this value. NOTE: These are NOT arguments that are guaranteed to be included in a request method. Whether or not they are is of no consequence here. It is for any argument that is not a parameter of every CpApiRequest.
                PossibleValues: 
                    'format_params': list -- In some situations, you will need part or all of a CpApiTuples.value string to be decided by a variable which defined in the destination api class. If you try to do this with e.g. ''.format(var_from_api_class), you will get an undefined error. This arg provides a workaround, for the sake of making this workflow as flexible as possible. Any of the strings nested inside a CpApiTuples.value (except for the id, which must NOT be dynamic in  nature) can include one or more sets of braces '{}' WITHOUT a Pythonic format method (i.e. fstring, str.format, etc. if you have the value here, it should be formatted by python using one of these methods. If this is the case, it will be expanded before our parser ever sees it.) If the '{}' is contained in a regular, unformatted string, then the parser will look for this param. If it is not set, the {} will be taken as a literal. If it is defined and has one or more unused values, the first unused value will be substituted. So, assuming this made a valid CpApiTuples.value, if you have ('99','mary {}', '{}', '{} {}',{format_params:['had_word','a_word','little_word','lamb_word']}), and the tuple is sent to MyApiImpl, its constructor will recieve the equivalent of ('99', 'mary {}', '{}', '{} {}') 
    """

#   TODO:
#       - update last parameter of each value tuple with the 'url_path' (the part after the '/')
#           - so far, only codeforces is correct

    CODEFORCES = ('00', 'codeforces', 0, '/api/{}', 'GET', {'format_params': []})
    CODECHEF = ('01', 'codechef', 0, '/') 
    TOPCODER = ('02', 'topcoder', 0, '/')
    LEETCODE = ('03', 'leetcode', 0, '/')
    PROJECT_EULER = ('04', '', '')
    GOOGLE_KICKSTART = ('05', '', '')
    CODEWARS = ('06', '', '')
    REPLY_CHALLENGES = ('07', '', '')
    KAGGLE_LEARN = ('08', '', '')
    HACKERRANK = ('09', 'hackerrank', 0, '')
    HACKEREARTH_POST_EVAL = ('10', ['api','hackerearth'], 0, 'v{}/partner/code-evaluation/submissions/'.format(version=4), 'POST')

class Api(object):

    """
    Description: Enum hybrid class that exposes an interface to the various "A-list" competitive progrsmming sites, via their apis if available, and if not, via any means necessary. 
    Values:
        
    """

#   TODO:
#       - update last parameter of each value tuple with the 'url_path' (the part after the '/')
#           - so far, only codeforces is correct

    @property
    def suffix(self):
        return self.__urlsuff__

    @suffix.setter
    def suffix(self, ndx:int):
        __urlsuffs__ = ['com', 'org', 'io', 'edu', 'net']
        self.__urlsuff__ = __urlsuffs__[ndx]

    @property
    def endpoints(self):
        return self.__endpoints_list

    @endpoints.setter
    def endpoints(self,*args, epls=None):
        self.__endpoints_list = []
        if type(epls) == None:
            self.__endpoints_list = epls
            

class CodeforcesApiMethodValues(Enum):
    """
    A comprehensive listing of all Codeforces api Methods supported by the program at a time.
    """
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
    """
    abstraction class used primarily as a container that holds the data type and related info for a parameter in an api method call
    """

    def __init__(self):
        __default_lowered_hintchoices_DO_NOT_CHANGE = [
            'str',
            'string',
            's',
            'st',
            'int',
            'integer',
            'i',
            'float',
            'floatingpoint',
            'floating point',
            'floating-point',
            'floating_point',
            'f',
            'fl',
            'fp',
            'f-p',
            'f_p',
            'f p',
            'double',
            'doubleprecisionint'
            'double precision int'
            'double-precision-int'
            'double_precision_int'
            'byte',
            'list',
            'ls',
            'll',
            'tuple',
            'tup',
            'tt',
            'set',
            'ss',
            'dict',
            'dictionary',
            'dd'
        ]
        self.user_hints_to_constructors_map = {}

    def __map_hint_to_func(self, hint:str, func:str):
        if type(hint) is not str or type(func) is not str:
            raise cfp_errors.CfpValueError()
        else:
            self.user_hints_to_functions_map[hint] = func
        
    def __add_hints_to_funcmap(self, *kv_tuples:tuple):
        for kvt in kv_tuples:
            if type(kvt) != tuple:
                raise cfp_errors.CfpTypeError
            elif kvt.count() != 2:
                raise cfp_errors.CfpValueError
            else:
                self.__flag_BOTH_STRINGS = True
                for i in kvt:
                    if type(i) != str:
                        self.__flag_BOTH_STRINGS = False
                else:
                    if self.__flag_BOTH_STRINGS == True:
                        # At this point we can be sure that kvt is a tuple containing exactly 2 string values
                        self.__map_hint_to_func(kvt[0], kvt[1])
                    else:
                        raise cfp_errors.CfpTypeError

    @property
    def user_hints_to_constructor_functions_map(self):

        return self.__hints_funcs_map

    @user_hints_to_constructor_functions_map.setter
    def user_hints_to_constructor_functions_map(self, val):
        """
        Accepts either a tuple containing a hint (str) and constructor ref (str, the name of the type's constructor), or else a list of these tuples
        """
        if not self.__hints_funcs_map:
            self.__hints_funcs_map = {}
        temp = self.user_hints_to_constructor_functions_map()
        if temp == None:
            temp = {}
        if type(val) == tuple:
            self.__hints_funcs_map = {}
            try:
                self.__add_hints_to_funcmap(val)
            except BaseException as e:
                if temp != {}:
                    self.__hints_funcs_map = temp
                    raise e
        elif type(val) == list:
            for i in val:
                try:
                    self.__add_hints_to_funcmap(i)
                except(e):
                    if temp != {}:
                        self.__hints_funcs_map
                        raise e

    @property
    def default_normalized_typehint_choices(self):
        """
        Setter is intentionally left out. This should be changed from inside the source code for any reason. If you are trying to change the values, then you may be getting this property confused with the 'normalized_typehint_choices' property which is meant to be added to and / or changed when needed (but has its own stipulations). This property is just an immutable list used as the initial values for that one.
        """
        return self.__def_lowered_hintchoices_DO_NOT_CHANGE

    @property
    def normalized_typehint_choices(self):
        """
        Setter is intentionally left out. This should be changed from inside the source code for any reason. If you are trying to change the values, then you may be getting this property confused with the 'normalized_typehint_choices' property which is meant to be added to and / or changed when needed (but has its own stipulations). This property is just an immutable list used as the initial values for that one.
        """
        return self.__lowered_hintchoices

    @normalized_typehint_choices.setter
    def normalized_typehint_choices(self, *args):
        hintlist = self.default_normalized_typehint_choices()
        for arg in args:
            if type(arg) == list:
                for item in arg:
                    hintlist.append(str(item))



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
            raise ValueError("""Type not directly supported. If you feel there has been a mistake, and you are SURE that the api is expecting the type you've provided, then try running the as_value() method instead""")
        return res
    
    def __resolve_for_params(self, *params:str, pt_choices:list=None, default=None):
        """
        Used to figure out the ParamType. This method is (and/or always should be called by any ParamType parse) called any time. 
        """
        pass

    def __resolve_for_paramlist(self, params:list, pt_choices:list=None, default=None):
        """
        Used to figure out the ParamType. This method is (and/or always should be called by any ParamType parse) called any time. 
        """
        pass

    def __resolve_for_paramdict(self, params:dict, pt_choices:list=None, default=None):
        """
        Used to figure out the ParamType. This method is (and/or always should be called by any ParamType parse) called any time. 
        """
        pass
    
    def resolve_for(*args, **kwargs):
        """Front end for the other 'resolve...' methods"""
        pass

    def set_type(self, typehint:str=None):
        if typehint is not None:
            self.type = self.check_type(typehint)

    def __init__(self):
        self
        pass

class ApiMethodParameter(object):
    """
    This is the class used to define a parameter for an api method. When a method object is defined, any parameters that this method takes will be declared as type api_method_parameter. It does not hold the value, it just checks that the value passes all of the specified constraints. 
    """
# REDO REDO REDO!!
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, namestr:str = None):
        self.__name = namestr

    @property
    def require(self) -> bool:
        return self.__require

    @require.setter
    def require(self, req:bool) -> None:
        self.__require = req

    @property
    def type(self) -> ParamTypes:
        return self.__type

    @type.setter
    def type(self,t:ParamTypes) -> None:
        self.__type = t

    @property
    def default_value(self) -> str:
        return self.__def_val
    
    @default_value.setter
    def default_value(self, dv:str) -> None:
        self.__def_val = dv

    @property
    def types_accepted(self)->dict:
        return self.__t_acc

    @types_accepted.setter
    def types_accepted(self, ta:dict)->dict:
        self.__t_acc = ta

    def __init__(self, name, def_val:object=None, required:bool=False, param_type:ParamTypes='obj', types_accepted:dict=None):
        """
        params:
            default_value: str <- Optional
                the value to which the parameter will be set if no value arg is given. 
            'required': bool <- (doubly!) Required
                whether or not to fail if the parameter is not given.
            types_accepted: dict(ParamTypes:function,...) <- Optional
                A dict specifying the types in which the parameter value(s) can be given. For any types accepted, a function must be provided to convert that type to the type needed. This is optional, and it is only for instances where you need a type not specified explicitly in param_type. Instead of using the OBJECT_SUBTYPE type, you can write a converter function which casts your type to one in ParamTypes.names, and give the type and converter in the dictionary. The converter needs to take the custom type as input and return 
                the expected type as output. There may or may not be a few default converters below or in their own module. Depends on whether or not I get time... 
                
            typehint set to obj as a catchall, as every type in python3 is a subtype of object (except object, which also works.) 
        """
        self.name(name)
        self.require(required)
        self.default_value(def_val)
        self.type(param_type)
        if types_accepted:
            self.types_accepted(types_accepted)
        if self.types_accepted:
            for k,v in types_accepted: 
                if self.parameter_type == k:
                    func = formatfuncstr(v,k)
                    _exec_st = ''.join('formatfuncstr_result = ', func)
                    try:
                        exec(_exec_st)
                    except NameError:
                        print("something went wrong while trying to execute {}".format(_exec_st))
                        return 1
                    if not self.formatfuncstr_result:
                        raise ValueError
                
            
class ReturnType(json.JSONEncoder):
    """
    Return type of an ApiMethod object.
    """
    def __init__(self):
        pass
    
class ResponseObject(object):
        
    def __init__(self,input):
        super.__init__()    
            
class ApiMethod(object):
    """
    A callable api method specified in an api. 
    """
    @property
    def parentapi(self):
        """
        For now it is hard-wired as Codeforces. Eventually, platform will support other comp. coding apis.
        This property is only in place for that eventuality, at which time the value will be added as a configuration option. The getter and setter defined here will obviously need altered as well. 
        """
        return 'codeforces.com/api/'
    
    @parentapi.setter
    def parentapi(self, arg):
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
        """
        sets parameters for an a
        """
        self._p_list = {}
        if len(args[1:-1]) == 0:
            pass
        elif len(args[1:-1]) == 1:
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
                        self._p_list[keys[i]] = vals[i]
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
    
    def __init__(self, params:list=None, paramstr:str=None)->ParamTypes:
        """Needs exactly one of the two args. accepts a string or a list of  parameter"""
        pass

    def is_member_of(self, api):
        #TODO: IMPLEMENT--the line below needs deleted. Filler, so the param is used and doesn't cause an error.
        print(api)
        pass


class CodeforcesApiMethod(ApiMethod):
    """
    Abstraction for a Codeforces Api method.
    """

#   TODO:
#       - implement call_string property / method. Currently set to \"pass\" below        

    @property
    def parentapi(self):
        """
        For now it is hard-wired as Codeforces. Eventually, platform will support other comp. coding apis.
        This property is only in place for that eventuality, at which time the value will be added as a configuration option. The getter and setter defined here will obviously need altered as well. 
        """
        return 'codeforces.com/api/'
    
    @parentapi.setter
    def parentapi(self, *args, **kwargs):
        click.echo('The current version of this program only supports codeforces.com. The `parent_api` property and its methods are only included to make provisions for future versions.')
        return False

    @property
    def conn_protocol(self):
        return self._c_proto

    @property
    def call_string(self):
        pass
        #self._cs = 
        
    def run_query():
        pass
    
    def __init__(self,*params:ApiMethodParameter)->ParamTypes:
        pass
    