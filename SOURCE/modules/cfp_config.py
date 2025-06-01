from dataclasses import dataclass
import os, typing
# from SOURCE.lib import libcfapi_utils
from .cfp_errors import CfpInitializationError, CfpTypeError, CfpUserInputError, CfpOverwriteNotAllowedError, CfpConfigurationError, CfpMethodInputError, CfpOSError, CfpPermissionDeniedError, CfpEncodingError, CfpValueError
from enum import Enum, Flag
from pathlib import Path

class Action(Flag):
    """Represents possible actions that can be used on a ConfigFile.sections list and ConfigSection.keys_values_dict"""
    UPDATE = 1
    OVERWRITE = 2
    EMPTY = 3
    REFRESH = 4
    INIT = 5

class AppConfigurationOptions(Enum):
    """
    This class can be used, when building a config, to describe all the possible options allowed in ypur config file. The dictionary keys correspond to the options allowed as l_values in the conffile. the values are stringified representations of those values.
    """
    pass
@dataclass
class ConfigSection:
    """This class represents a section of a config file. Config options that are related should be located together in a section, represented as keys and values in the keys_vals_dict property of a ConfigSection object."""

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
    def values(self) -> dict:
        """This is where the configuration options are stored as keys and values."""
        return self.__config_kvs

    @values.setter
    def values(self, action_values_list) -> None:
        """
        The param passed into this function needs to be a list with exactly 2 items. The first must be an Action (see the Flag enum above). The second MUST be a dict containing the keys and values to either add to the list (Action.UPDATE) or replace the current list (Action.OVERWRITE)
        """
        input_bad = False
        if type(action_values_list) == list and len(action_values_list) == 2 and action_values_list[0] == Action.OVERWRITE and type(action_values_list[1]) == dict or type(action_values_list) == list and len(action_values_list) == 2 and action_values_list[0] == Action.UPDATE and type(action_values_list[1]) == dict or type(action_values_list) == list and action_values_list[0] == Action.EMPTY and len(action_values_list) == 1 or type(action_values_list) == list and len(action_values_list) == 2 and action_values_list[0] == Action.INIT and type(action_values_list[1]) == dict:
            for k,v in action_values_list[1].items():
                if type(k) != str or type(v) != str:
                    input_bad = True
            if input_bad == False:
                if action_values_list[0] == Action.OVERWRITE:
                    self.__config_kvs = action_values_list[1]
                elif action_values_list[0] == Action.INIT:
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

    def __init__(self, name: str, description: str, keys_vals_dict: dict={}):

        self.name = name
        self.description = description
        self.values = [Action.INIT, keys_vals_dict]

    def update(self, new_vals: dict):
        self.values = [Action.UPDATE, new_vals]
        return True

    def overwrite(self, new_vals: dict):
        self.values = [Action.OVERWRITE, new_vals]
        return True
class Configuration(object):
    """This class represents a configuration, linked to a config file, made up primarily of ConfigSection objects representing the sections of that configuration."""

    @property
    def sections(self) -> 'list[ConfigSection]':
        """This is a list of ConfigSection objects, containing all the sections of the config."""
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
        This is a list of 0 ar more ConfigSection objects to append to the sections list.
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
                    if type(a) == ConfigSection:
                        self.__sectslist_.append(a)
                    else:
                        raise CfpTypeError()
            else:
                raise CfpUserInputError
        elif action_and_args[0] == Action.OVERWRITE:
            self.__sectslist_ = []
            for a in action_and_args[1]:
                if type(a) == ConfigSection:
                    self.__sectslist_.append(a)
        elif action_and_args[0] == Action.EMPTY:
            self.__sectslist_ = []
        elif action_and_args[0] == Action.REFRESH:
            self.__secnames = self.__get_section_names_from_conffile()
            for name in self.__secnames:
                pass
        elif action_and_args[0] == Action.INIT:
            self.__sectslist_ = []
            for a in action_and_args[1]:
                if type(a) == ConfigSection:
                    self.__sectslist_.append(a)
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


    def __init__(self, location_dirpath: str, filename: str, sects_list: list=[]):
        self.sections = [Action.INIT, sects_list]
        self.filename = filename
        self.location_dirpath = location_dirpath

    def create_config_file(self) -> bool:
        """
        If config file does not exist, this creates it and returns True. If it does exist, it just returns True. If it does not exist and cannot be created, it raises an error.
        """
        slash = self.__get_slash_type()
        filepath = self.location_dirpath + slash + self.filename
        if Path.exists(filepath):
            return True
        else:
            try:
                with open(filepath, 'x'):
                    pass
            except PermissionError:
                raise CfpPermissionDeniedError
            except OSError:
                raise CfpOSError
            except UnicodeError:
                raise CfpEncodingError
            except TypeError:
                raise CfpTypeError
            except ValueError:
                raise CfpValueError
            return True

    def add_section_to_config_file(self, section_name: str, kv_list: list[str]) -> bool:
        """
        Either writes a section to the end of the config file with \'section_name\' as the name and each line in \'kv_list\' on its own line, or raises an error if it cannot be written. Each line must be of the format \'key = value\' or else an CfpMethodInputError will be raised.
        """
        try:
            slash = self.__get_slash_type()
            filepath = self.location_dirpath + slash + self.filename
            with open(filepath, 'w') as file:
                name_str = '[[' + section_name + ']]\n'
                file.write(name_str)
                for line in kv_list:
                    if '=' in line:
                        file.write(line + '\n')
                    else:
                        raise CfpMethodInputError('One or more lines passed to this method are formatted incorrectly. They must be of the form \'key = value\'.')
        except PermissionError:
            raise CfpPermissionDeniedError
        except OSError:
            raise CfpOSError
        except UnicodeError:
            raise CfpEncodingError
        except TypeError:
            raise CfpTypeError
        except ValueError:
            raise CfpValueError
        return True

    def get_section_from_config_file(self)  -> ConfigSection:
        pass

    def __get_section_names_from_conffile(self) -> "list[tuple]":
        sects_ls = []
        if os.name == 'posix':
            slash = '/'
        else:
            slash = '\\'
        lst = [self.location_dirpath, self.filename]
        _filelocation = slash.join(lst)
        with open(_filelocation, 'r') as file:
            for i, line in enumerate(file):
                cleanln = line.lstrip().rstrip()
                if cleanln.startswith("[[") and cleanln.endswith("]]"):
                    sectup = (i,cleanln[2:-2])
                    sects_ls.append(sectup)
        return sects_ls

    def __get_section_kvs_from_conffile(self, section_name: str) -> "list[tuple]":
        """
        retrieves a section from a conf file and returnsit as a python dictionary
        TODO: fix it so it works
        """

        # if section_entered is True, the [[section_name]] line has already been reached, so the next [[section]] line will be the end of the section.
        section_entered = False

        if os.name == 'posix' or os.name == 'java':
            slash = '/'
        else:
            slash = '\\'
        
        lst = [self.location_dirpath, self.filename]
        path = slash.join(lst)
        tuples_list = []

        with open(path, 'r') as file:
            for i, line in enumerate(file):
                cleanln = line.strip()
            
                pattern = '[[' + section_name + ']]'
                if cleanln == pattern:
                    section_entered == True

                if section_entered == True:
                    if cleanln.startswith('[['):
                        return tuples_list
                    else:
                        split = cleanln.split('=')
                        if len(split) <= 1:
                            raise CfpUserInputError('The format of your config file has 1 or more errors. Every line must either start with "[[" or be of the form "key = value. No blank lines!!"')
                        tup = (split[0].strip, split[1].strip)
                        tuples_list.append(tup)

            return tuples_list

    def __get_slash_type(self):
        if os.name == 'posix' or os.name == 'java':
            slash = '/'
        elif os.name == 'nt':
            slash = '\\'
        else:
            raise AppConfigurationOptions
        return slash

            # for i, line in enumerate(file):
            #     cleanln = line.lstrip().rstrip()
            #     if cleanln.startswith("[[") and cleanln.endswith("]]"):
            #             pass
            #     else:
            #         k_eq_v_list = cleanln.split()
            #         size = len(k_eq_v_list)
            #         if size >= 3:
            #             if k_eq_v_list[1] == '=':
            #                 # need to finish
            #                 key = k_eq_v_list[0]
            #                 val_str = ''
            #                 for word in k_eq_v_list:
            #                     if word >= 2:
            #                         val_str = val_str + ' ' + word
            #             else:
            #                 raise CfpConfigurationError('There is a formatting error in your config file. Note that all l_values need to be one word, and there must be a space on each side of the "=", so that each line looks like this: "oneword = one or more words"')
            #         else:
                        # pass

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
        A private function that takes in a ConfigSection and writes it to a conf file.
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
