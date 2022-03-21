import os, typing
from ..lib import libcfapi_utils
from .cfp_errors import CfpInitializationError, CfpUserInputError, CfpOverwriteNotAllowedError
from enum import Enum

class AppConfigurationOptions(Enum):
    '''
    Allowed config options. The names correspond to the options allowed as l_values in the conffile. the values are stringified representations
    '''
class Section:
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
                self.__sectslist_.append(a)
        elif action == 'overwrite':
            self.__sectslist_ = []
            for a in args:
                self.__sectslist_.append(a)
        elif action == 'empty':
            self.__sectslist_ = []
        elif action == 'refresh':
            self.__get_sections_from_conffile()

    def __get_sections_from_conffile(self):
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r')    

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
                if type(iter) == list:


            super().__init__(conf_or_iter, **kvpairs)

    def __init__(self, **kvpairs):
        super().__init__(**kvpairs)
