import configparser
from dataclasses import dataclass
import os
from . import libcf_api.libcfapi_constants as apic, libcf_api.libcfapi_utils as apiu
from pathlib import Path



class Option(str):
    # ::TAGS:: |:Trend:|:beat:|:melon:|:moth:| 
    """
    Type for a kwarg string in a python functions t
    """
    
class TagLocker(dict):
    """
    Description: dictionary of format {tagName(string): locationsWhereTagExists(List[hashOfLocation]), ...}: 
    """
    def __init__(self):
        super().__init__()
    
@dataclass
class Location:
    '''
    represents a location in a python package, module, or script 
    '''

    @property
    def base_type(self):
        return self.__base_type_

    @base_type.setter
    def base_type(self,val):
        good_vals = ['P','M','S']
        if val not in goodvals:
            raise ValueError()
        
        self.__base_type_ = val

    @property
    def packagename(self):
        return self.__packagename_

    @packagename.setter
    def packagename(self,val):
        self.__packagename_ = val

    @property
    def modulename(self):
        return self.__modulename_

    @modulename.setter
    def modulename(self,val):
        self.__modulename_ = val

    @property
    def methodname(self):
        return self.__methodname_

    @methodname.setter
    def methodname(self,val):
        self.__methodname_ = val

    @property
    def funcname(self):
        return self.__funcname_

    @funcname.setter
    def funcname(self,val):
        self.__funcname_ = val

    @property
    def filename(self):
        return self.__filename_

    @v.setter
    def filename(self,val):
        self.__filename_ = val

    @property
    def linenum(self):
        return self.__linenum_

    @linenum.setter
    def linenum(self,val):
        self.__linenum_ = val


    def __init__(self, locationstring:str, basetype=File)
class TagTools:
    
    def __init__():
        pass
    
class MetaUtils(object):

    def __init__():
        print('This class is not meant to be instantiated. If you need the exposed functionalities, try calling the methods as class methods.')
        return False
        
    @classmethod
    def install_create_home_dir():
        start_dir = os.cwd()
        if ctx_base is not None:
            self.ctx_parent_entry = os.scandir(apic.CFP_CTX)
        if os.is_dir(ctx_base): 
            os.chdir(ctx_base)
        else
            pass
        
    def cf_config_tool(self,action=None):
        configpath = 
        if action == None:
            return configpath

class CtxPathResolver:
    
    @property
    def ctx_dirpath(self):
        return self._ctx_dirpath
    
    @ctx_dirpath.setter
    def ctx_dirpath(path: Path):
        self._ctx_dirpath = path  
        
    def __init__(self, path:Path=None):
        self.ctx_dirpath(path) 
