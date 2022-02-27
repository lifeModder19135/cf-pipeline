

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

class API_Method_Parameter(object):
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
            
            
class api_method(object):
    '''
    A callable api method specified in an api. 
    '''
    
    @property
    def call_string():
        pass
        
    def call_method():
        pass
    
    