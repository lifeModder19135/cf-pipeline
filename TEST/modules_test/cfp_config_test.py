from ...SOURCE.modules.cfp_config import ConfFileSection, ConfigFile, Action

def create_conffilesection_test():

    section = ConfFileSection('test section', 'a test section', Action.UPDATE, {'test_key': 'test_value'})
    assert type(section) == ConfFileSection