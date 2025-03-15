from dataclasses import dataclass
import os, typing
from ..lib import libcfapi_utils
from .cfp_errors import CfpInitializationError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpConfigurationError, CfpMethodInputError
from enum import Enum, Flag

class Action(Flag):
    """Represents possible actions that can be used on a ConfigFile.sections list"""
    UPDATE = 1
    OVERWRITE = 2
    EMPTY = 3
    REFRESH = 4

class AppConfigurationOptions(Enum):
    """
    Allowed config options. The dictionary keys correspond to the options allowed as l_values in the conffile. the values are stringified representations
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
    def keys_vals_dict(self, action: Action, kvdict:dict) -> None:
        input_bad = False
        if type(kvdict) == dict:
            for k,v in kvdict.items():
                if type(k) != str or type(v) != str:
                    input_bad = True
            if input_bad == False:
                if action == Action.OVERWRITE:
                    self.__config_kvs = kvdict
                elif action == Action.UPDATE:
                    for k,v in kvdict.items():
                        for key in self.__config_kvs.keys():
                            if k == key:
                                self.__config_kvs[key] = v
                                kvdict.pop(k)
                    self.__config_kvs.update(kvdict)
                else:
                    raise CfpUserInputError


    def __init__(self, name: str, description: str, action: Action, keys_vals_dict: dict={}):

        self.name(name)
        self.description(description)
        self.keys_vals_dict(action, keys_vals_dict)

class ConfigFile(object):

    @property
    def sections(self) -> 'list[ConfFileSection]':
        """This is a list of ConfFileSection objects, containing the names of all the sections of the config."""
        if not self.__sectslist_:
            self.__sectslist_ = []
        return self.__sectslist_

    @sections.setter
    def sections(self, action: str = 'update', args: list=None)->None:
        """"
        Sets the sections list. 
        The args parameter is a list of 0 ar more ConfFileSection objects to append to the sections list.
        The action parameter holds the action taken on the __sectslist_.
        Possible actions are:
          - update: append args to __sectslist_
          - overwrite: clear __sectslist_ and then add args to the empty list
          - empty: clear __sectslist_ and leave it empty: args are not used
          - refresh: stillworking on it
        """
        #TODO: finish me
        if not self.__sectslist_:
            self.__sectslist_ = []
        if action == Action.UPDATE:
            for a in args:
                if type(a) == ConfFileSection:
                    self.__sectslist_.append(a)
                else:
                    raise CfpTypeError()
        elif action == Action.OVERWRITE:
            self.__sectslist_ = []
            for a in args:
                self.__sectslist_.append(a)
        elif action == Action.EMPTY:
            self.__sectslist_ = []
        elif action == Action.REFRESH:
            self.__secnames = self.__get_section_names_from_conffile()
            for name in self.__secnames:
                pass

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

    def __init__(self, location_dirpath: str, filename: str, sects: list=[], action: Action =Action.UPDATE):
        self.sections(sects, 'update')
        self.filename(filename)
        self.location_dirpath(location_dirpath)

    def __get_section_names_from_conffile(self) -> "list[tuple]":
        sects_ls = []
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r') as file:
            for i, line in enumerate(file):
                cleanln = line.lstrip().rstrip()
                if cleanln.startswith("[[") and cleanln.endswith("]]"):
                    sectup = (i,cleanln[2:-2])
                    sects_ls.append(sectup)
        return sects_ls

    def __get_section_kvs_from_conffile(self) -> "list[tuple]":
        __kv_dict = {}
        _filelocation = '/'.join(self.location_path(),self.filename())
        with open(_filelocation, 'r') as file:
            for i, line in enumerate(file):
                cleanln = line.lstrip().rstrip()
                if cleanln.startswith("[[") and cleanln.endswith("]]"):
                        pass
                else:
                    k_eq_v_list = cleanln.split()
                    size = len(k_eq_v_list)
                    if size >= 3:
                        if k_eq_v_list[1] == '=':
                            # need to finish
                            key = k_eq_v_list[0]
                            val_str = ''
                            for word in k_eq_v_list:
                                if word >= 2:
                                    val_str = val_str + ' ' + word
                        else:
                            raise CfpConfigurationError('There is a formatting error in your config file. Note that all l_values need to be one word, and there must be a space on each side of the "=", so that each line looks like this: "oneword = one or more words"')
                    else:
                        pass

    def __write_dict_to_conf_file(self, input_dict:dict, filelocation='use_obj_attributes'):
        """
        Dict passed in must contain only section identifiers such as:
                key = '[[section_name]]', value = 'SECTION'
        or values in a section such as:
                key = 'foo', value = 'bar'
        all kvs between two sections will be written to the earlier section.
        NOTE: first kv in dict MUST be a section identifier
        """
        if filelocation == 'use_obj_attributes':
            filelocation = '/'.join(self.location_path(),self.filename())
        elif type(filelocation) is not str or filelocation[0] != '/':
            raise CfpMethodInputError('Invalid path to config file')
        else:
            if not os.path.exists(filelocation):
                open(filelocation).close
            input_dict[0].lstrip().rstrip()
            if input_dict[0].startswith('[[') and input_dict[0].endswith(']]'): 
                for k,v in input_dict:
                    if k.startswith('[[') and k.endswith(']]') and v == 'SECTION':
                        with open(filelocation) as f:
                            f.write(k)
                    else:
                        with open(filelocation) as f:
                            f.write('  ' + k + ' = ' + v)
            else:
                raise CfpMethodInputError('First kv in input dict must be a section identifier')
    def __write_section_to_conf_file():
        pass
            
        
                            

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
