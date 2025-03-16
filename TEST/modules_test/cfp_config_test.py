from SOURCE.modules.cfp_config import ConfFileSection, ConfigFile, Action

def create_conffilesection_test():

    section = ConfFileSection('test section', 'a test section', Action.UPDATE, {'test_key': 'test_value'})
    assert type(section) == ConfFileSection
    assert section.name == 'test section'
    assert section.description == 'a test section'
    assert type(section.keys_vals_dict) == dict