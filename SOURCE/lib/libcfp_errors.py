
class CfpError(Exception):
    def __init__(self, *msgs, t_str=None, callback_error_type=None):
        self._type = t_str 
        print('Cf-Pipeline: Error: {f_type}: '.format(f_type=self._type))
        self.__print_messages(msgs)
        if callback_error_type.isinstance(Exception):
            callback_error_type.__init__()
        else:
            super.__init__()
            
    @property
    def type(self):
        return self.__type
        
    @type.setter
    def type(self, t_str: str):
        self.__type = t_str
     
        
    def __print_messages(*msgs):
        for m in msgs:
            print(m)
        return True
    
class CfpSetupError(CfpError):
    def __init__(self,  *msgs, callback_error_type=None):
        cet = callback_error_type
        super.__init__(msgs, t_str='Setup error', callback_error_type=cet )
            
class CfpCtxDirectoryMissingError(CfpError, OSError):

    __default_msg = """One or more of the context directories used by cf_pipeline is missing, or else the application is misconfigured.
                            
        Cf_pipeline comes with a built-in tool for finding out where the program expects these directories to be located.
                                       
        Change directories to the location where you want this tool (and in which you have write permission) and type the command ``cf_config_tool``.
                                       
        There should now be a file `config_script.py` in the directory. If you cat this file, you will find an assortment of functions.
                                       
        Each of these functions returns a path. Make sure that each of these directories exists.
                                       
        Alternatively, you can rebuild the app, but be aware that any previous configurations will likely be lost.
                                       
        Check your configuration, making needed changes, and restart the application"""

    def __init__(self, msgs, callback_error_type=None):
        cet = callback_error_type
        if not msgs:
            super.__init__(self.__default_msg, t_str='Path error', callback_error_type=cet)
        else:
            super.__init__(msgs, t_str='Path error', callback_error_type=cet)
        
        
        
        
        
