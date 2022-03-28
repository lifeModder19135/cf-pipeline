import configparser
import os
from SOURCE.lib.libcf_api import libcfapi_constants as apic, libcfapi_utils as apiu
from pathlib import Path
from SOURCE.modules.cfp_errors import CfpInitializationError




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
    

class Location:
    """
    represents a location in a python package, module, or script 
    """

    @property
    def base_type(self):
        """
        required - must be set to one of the following: 
          'P' for package-based,
          'M' for module-based, or
          'S' for script-based locations
        """
        return self.__base_type_

    @base_type.setter
    def base_type(self,val):
        good_vals = ['P','M','S']
        if val not in good_vals:
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
    def scriptname(self):
        return self.__scriptname_

    @scriptname.setter
    def scriptname(self,val):
        self.__scriptname_ = val

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

    def __p_init(self, pname:str, mname:str, fname:str, lnum:int, funcname:str=None, methodname:str=None):
        self.packagename(pname)
        self.__m_init__(mname, fname, lnum, funcname, methodname)

    def __m_init(self, mname:str, fname:str, lnum:int, funcname:str=None, methodname:str=None):
        if funcname != None and methodname != None:
            raise CfpInitializationError('The funcname and methodname properties of the Location class are mutually exclusive. Both cannot be set within a single object. Check the syntax in your setter.')
        elif funcname != None:
            self.funcname(funcname)
        elif methodname != None:
            self.methodname(methodname)
        self.modulename(mname)
        self.filename(fname)
        self.linenum(lnum)        

    def __s_init(self, sname:str, lnum:int, funcname:str=None, methodname:str=None):
        if funcname != None and methodname != None:
            raise CfpInitializationError('The funcname and methodname properties of the Location class are mutually exclusive. Both cannot be set within a single object. Check the syntax in your setter.')
        elif funcname != None:
            self.funcname(funcname)
        elif methodname != None:
            self.methodname(methodname)
        self.scriptname(sname)
        self.linenum(lnum)        


    def __init__(self, loctype:str, *args:str):
        try:
            if loctype == 'P':
                self.__p_init(args)
            elif loctype == 'M':
                self.__m_init(args)
            elif loctype == 'S':
                self.__s_init(args)
            else:
                raise ValueError
        except ValueError:
            __initerror_message = "Check arguments and try again."
            raise CfpInitializationError(__initerror_message)

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
        """
        TODO: Implement or delete; currently this is just half of an idea that I've long since forgotten.
            check config module; it may still be needed, as 'action' IS used there.
        """
        configpath = ''
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
