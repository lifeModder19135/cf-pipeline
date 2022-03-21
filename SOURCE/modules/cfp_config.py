import os, typing
from ..lib import libcfapi_utils
<<<<<<< Updated upstream
from .cfp_errors import CfpInitializationError, CfpUserInputError, CfpOverwriteNotAllowedError
=======
from .cfp_errors import CfpInitializationError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError
>>>>>>> Stashed changes
from enum import Enum

class AppConfigurationOptions(Enum):
    '''
    Allowed config options. The names correspond to the options allowed as l_values in the conffile. the values are stringified representations
    '''
<<<<<<< Updated upstream
class Section:
=======
class ConfFileSection:
>>>>>>> Stashed changes
    pass

class ConfigFile(object):


    @property
    def sections(self) -> 'list[Section]':
        '''This is a list of strings containing the names of all the sections of the config.'''
        if not self.__sectslist_:
            self.__sectslist_ = []
        return self.__sectslist_

    @sections.setter
    def sections(self,action, *args)->None:
        #TODO: finish me
        if not self.__sectslist_:
            self.__sectslist_ = []
        if action == 'update':
            for a in args:
<<<<<<< Updated upstream
                self.__sectslist_.append(a)
=======
                if type(a) == ConfFileSection:
                    self.__sectslist_.append(a)
                else:
                    raise CfpTypeError()
>>>>>>> Stashed changes
        elif action == 'overwrite':
            self.__sectslist_ = []
            for a in args:
                self.__sectslist_.append(a)
        elif action == 'empty':
            self.__sectslist_ = []
        elif action == 'refresh':
            self.__get_sections_from_conffile()

<<<<<<< Updated upstream
    def __get_sections_from_conffile(self):
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r')    
=======
    @property
    def location_dirpath(self) -> str:
        return self.__locdirpath

    @location_dirpath.setter
    def location_dirpath(self, lp) -> None:
        self.__locdirpath = lp

    @property
    def filename(self) -> str:
        return self.__file_name

    @filename.setter
    def filename(self, fname) -> None:
        self.__file_name = fname

    def __get_sections_from_conffile(self):
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r') as cfgfile:
            for line in cfgfile:
                if str(line).isspace:
                    continue
        

    def __parse_conffile(self):
>>>>>>> Stashed changes

class AppConfiguration(typing.dict):
    '''
    dict with config option names and values
    '''
    # TODO:

    def __init__(self, conf_dict:dict=None, iter:typing.Iterable=None, **kvpairs):
        if conf_dict == None and iter == None:
            super().__init__(**kvpairs)
        else:
            if conf_dict:
                if iter:
                    raise CfpInitializationError
                else:
                    for k,v in conf_dict:
                        pass
                        # TODO: ^^
            if iter:
<<<<<<< Updated upstream
                if type(iter) == list:


            super().__init__(conf_or_iter, **kvpairs)
=======
                if type(iter) == list or type(iter) == tuple:
                    for node in iter:
                        if type(node) != list and type(node) != tuple:
                            raise CfpTypeError()

            super().__init__(conf_dict, iter, **kvpairs)
>>>>>>> Stashed changes

    def __init__(self, **kvpairs):
        super().__init__(**kvpairs)
