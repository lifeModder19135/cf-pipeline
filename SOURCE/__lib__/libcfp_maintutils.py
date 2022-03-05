import os
from .libcf-api.libcfapi_constants import CFP_CONTEXT_DIRECTORY_BASE as ctx_base, CFP_CONTEXT_DIRECTORY_NAME as ctx_dirname
from pathlib import Path

class Option(str):
    """
    Type for a kwarg string in a python functions t
    """
    
class TagLocker(dict):
    """
    
    Args:
        dict (_type_): _description_
    """
    
class TagTools:
    
    def __init__():
        pass
    
class MetaUtils(object):

    def __init__():
        print('This class is not meant to be instantiated. If you need the exposed functionalities, try calling the methods as class methods.')
        return False
        
    @classmethod
    def __install_create_home_dir():
    start_dir = os.cwd()
    if ctx_base is not None:
        self.ctx_parent_entry: os.DirEntry = os.scandir(ctx_dir)
    if os.is_dir(ctx_base): 
        os.chdir(ctx_base)
    else
        pass
        
    def cf_config_tool(self):
    
class CtxPathResolver:
    
    @property
    def ctx_dirpath(self):
        return self._ctx_dirpath
    
    @ctx_dirpath.setter
    def ctx_dirpath(path: Path):
        self._ctx_dirpath = path  
        
    def __init__(self, path:pathlib.Path=None):
        self.ctx_dirpath(path) 
