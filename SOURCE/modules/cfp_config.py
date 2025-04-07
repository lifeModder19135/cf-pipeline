from dataclasses import dataclass
import os, typing
# from SOURCE.lib import libcfapi_utils
from .cfp_errors import CfpInitializationError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpConfigurationError, CfpMethodInputError
from enum import Enum, Flag

class Action(Flag):
    """Represents possible actions that can be used on a ConfigFile.sections list and ConfFileSection.keys_values_dict"""
    UPDATE = 1
    OVERWRITE = 2
    EMPTY = 3
    REFRESH = 4

class AppConfigurationOptions(Enum):
    """
    This class can be used, when building a config, to describe all the possible options allowed in ypur config file. The dictionary keys correspond to the options allowed as l_values in the conffile. the values are stringified representations of those values.
    """
    pass
@dataclass
class ConfFileSection:
    """This class represents a section of a config file. Config options that are related should be located together in a section, represented as keys and values in the keys_vals_dict property of a ConfFileSection object."""

    __name_=''
    __config_kvs = {}
    
    @property
    def name(self) -> str:
        """The name given to the section. This can be used to identify the section later."""
        return self.__name_

    @name.setter
    def name(self, val) -> None:
        self.__name_ = val

    @property
    def description(self) -> str:
        """This is a string that should be a snall paragraph that describes the section and what the keys and values represent."""
        return self.__descr

    @description.setter
    def description(self, val) -> None:
        self.__descr = val

    @property
    def keys_vals_dict(self) -> str:
        """This is where the configuration options are stored as keys and values."""
        return self.__config_kvs

    @keys_vals_dict.setter
    def keys_vals_dict(self, action_values_list) -> None:
        """
        The param passed into this function needs to be a list with exactly 2 items. The first must be an Action (see the Flag enum above). The second MUST be a dict containing the keys and values to either add to the list (Action.UPDATE) or replace the current list (Action.OVERWRITE)
        """
        input_bad = False
        if type(action_values_list) == list and len(action_values_list) == 2 and action_values_list[0] == Action.OVERWRITE and type(action_values_list[1]) == dict or type(action_values_list) == list and len(action_values_list) == 2 and action_values_list[0] == Action.UPDATE and type(action_values_list[1]) == dict or type(action_values_list) == list and action_values_list[0] == Action.EMPTY and len(action_values_list) == 1:
            for k,v in action_values_list[1].items():
                if type(k) != str or type(v) != str:
                    input_bad = True
            if input_bad == False:
                if action_values_list[0] == Action.OVERWRITE:
                    self.__config_kvs = action_values_list[1]
                elif action_values_list[0] == Action.UPDATE:
                    for k,v in action_values_list[1].items():
                        for key in self.__config_kvs.keys():
                            if k == key:
                                self.__config_kvs[key] = v
                                # action_values_list[1].pop(k)
                    self.__config_kvs.update(action_values_list[1])
                elif action_values_list[0] == Action.EMPTY:
                    self.__config_kvs = []   
            else:
                raise CfpUserInputError
        else: 
            raise CfpUserInputError

    def __init__(self, name: str, description: str, action: Action, keys_vals_dict: dict={}):

        self.name = name
        self.description = description
        self.keys_vals_dict = [action, keys_vals_dict]

class ConfigFile(object):
    """This is the class representation of a config file. It contains metadata, including the path to the file, and a list of ConfFileSection objects, which make up the content of the file."""

    @property
    def sections(self) -> 'list[ConfFileSection]':
        """This is a list of ConfFileSection objects, containing the names of all the sections of the config."""
        if not self.__sectslist_:
            self.__sectslist_ = []
        return self.__sectslist_

    @sections.setter
    def sections(self, action_and_args: list) -> None:
        """
        Sets the sections list. 
        The paramater is a list with either 1 or 2 items.
        the first item is of type Action. If it is Action.EMPTY, it will be the only item. 
        Anything else will have a second item. This must be a list.
        This is a list of 0 ar more ConfFileSection objects to append to the sections list.
        The action item holds the action taken on the __sectslist_.
        Possible actions are:
          - update: append args to __sectslist_
          - overwrite: clear __sectslist_ and then add args to the empty list
          - empty: clear __sectslist_ and leave it empty: args are not used
          - refresh: still working on it. Not yet available.
        """
        #TODO: finish me
        # if not self.__sectslist_:
        #     self.__sectslist_ = []
        if not hasattr(self, '__sectslist_'):
            self.__sectslist_ = []
        if action_and_args[0] == Action.UPDATE:
            if type(action_and_args[1]) == list:
                for a in action_and_args[1]:
                    if type(a) == ConfFileSection:
                        self.__sectslist_.append(a)
                    else:
                        raise CfpTypeError()
            else:
                raise CfpUserInputError
        elif action_and_args[0] == Action.OVERWRITE:
            self.__sectslist_ = []
            for a in action_and_args[1]:
                if type(a) == ConfFileSection:
                    self.__sectslist_.append(a)
        elif action_and_args[0] == Action.EMPTY:
            self.__sectslist_ = []
        elif action_and_args[0] == Action.REFRESH:
            self.__secnames = self.__get_section_names_from_conffile()
            for name in self.__secnames:
                pass
        else:
            raise CfpUserInputError

    @property
    def location_dirpath(self) -> str:
        """This is the absolute path to the directory of the config file on the end user's system. 'location_dirpath' + 'filename' should be the absolute path in full."""
        return self.__locdirpath

    @location_dirpath.setter
    def location_dirpath(self, lp) -> None:
        self.__locdirpath = lp

    @property
    def filename(self) -> str:
        """ This is the name of the config file. It should include the file extension if there is one. 'location_dirpath' + 'filename' should be the absolute path in full."""
        return self.__file_name

    @filename.setter
    def filename(self, fname) -> None:
        self.__file_name = fname

    def __init__(self, location_dirpath: str, filename: str, action_sects_list: list=[]):
        self.sections = action_sects_list
        self.filename = filename
        self.location_dirpath = location_dirpath

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
        """
        retrieves a section from a conf file and returnsit as a python dictionary
        TODO: fix it so it works
        """
        __kv_dict = {}
        if os.name == 'posix' or os.name == 'java':
            self._filelocation = '/'.join(self.location_path(),self.filename())
        elif os.name == 'nt':
            self._filelocation = '\\'.join(self.location_path(),self.filename())
        with open(self._filelocation, 'r') as file:
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
        This is a private function that takes a python dictionary and writes it to a conf file. It must be formatted as described below.
        TODO: fix me
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
        """
        A private function that takes in a ConfFileSection and writes it to a conf file.
        TODO: write me
        """
        pass
            
        
                            

# class AppConfiguration(typing.__dict__):
#     """
#     dict with config section names and inner dictionaries containing config opptions and values
#     """
#     # TODO:
#     #    - needs logic to check inner dicts and set values to class properties
#     #    - need to define properties

#     def __init__(self, conf_dict:dict=None, **kvpairs):
#         if conf_dict == None:
#             super().__init__(**kvpairs)
#         else:
#             super().__init__(conf_dict, **kvpairs)
