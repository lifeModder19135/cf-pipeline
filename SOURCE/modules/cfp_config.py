from dataclasses import dataclass
import os, typing
from ..lib import libcfapi_utils
from .cfp_errors import CfpInitializationError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError
from enum import Enum

class AppConfigurationOptions(Enum):
    """
    Allowed config options. The names correspond to the options allowed as l_values in the conffile. the values are stringified representations
    """
@dataclass
class ConfFileSection:
    
    @property
    def name(self) -> str:
        return self.__name_

    @name.setter
    def name(self, val) -> None:
        self.__name_ = val

    @property
    def description(self) -> str:
        return self.__descr

    @description.setter
    def description(self, val) -> None:
        self.__descr = val

    @property
    def keys_vals_dict(self) -> str:
        return self.__config_kvs

    @keys_vals_dict.setter
    def keys_vals_dict(self, action:str, kvdict:dict) -> None:
        input_bad = False
        if type(kvdict) == dict:
            for k,v in kvdict.items():
                if type(k) != str or type(v) != str:
                    input_bad = True
            if input_bad == False:
                if action == "overwrite":
                    self.__config_kvs = kvdict
                elif action == "update":
                    for k,v in kvdict.items():
                        for key in self.__config_kvs.keys():
                            if k == key:
                                self.__config_kvs[key] = v
                                kvdict.pop(k)
                    self.__config_kvs.update(kvdict)
                else:
                    raise CfpUserInputError

class ConfigFile(object):

    @property
    def sections(self) -> 'list[ConfFileSection]':
        """This is a list of ConfFileSection objects, or possibly strings (still undecided), containing the names of all the sections of the config."""
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
                if type(a) == ConfFileSection:
                    self.__sectslist_.append(a)
                else:
                    raise CfpTypeError()
        elif action == 'overwrite':
            self.__sectslist_ = []
            for a in args:
                self.__sectslist_.append(a)
        elif action == 'empty':
            self.__sectslist_ = []
        elif action == 'refresh':
            self.__secnames = self.__get_section_names_from_conffile()

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

    def __get_section_names_from_conffile(self) -> "list[tuple]":
        sects_ls = []
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r') as file:
            for i,line in enumerate(file):
                cleanln = line.lstrip().rstrip()
                if cleanln.startswith("[[") and cleanln.endswith("]]"):
                    sectup = (i,cleanln[2:-2])
                    sects_ls.append(sectup)
        return sects_ls


class AppConfiguration(typing.dict):
    """
    dict with config section names and inner dictionaries containing config opptions and values
    """
    # TODO:
    #    - needs logic to check inner dicts and set values to class properties
    #    - need to define properties

    def __init__(self, conf_dict:dict=None, **kvpairs):
        if conf_dict == None:
            super().__init__(**kvpairs)
        else:
            super().__init__(conf_dict, **kvpairs)
