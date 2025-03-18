from SOURCE.modules.cfp_config import ConfFileSection, ConfigFile, Action

def test_create_conffilesection_test():

    section = ConfFileSection('test section', 'a test section', Action.UPDATE, {'test_key': 'test_value'})
    assert type(section) == ConfFileSection
    assert section.name == 'test section'
    assert section.description == 'a test section'
    assert type(section.keys_vals_dict) == dict

def test_create_ConfigFile_test():
    section_1 = ConfFileSection('test section 1', 'a test section', Action.UPDATE, {'test_key': 'test_value'})
    section_2 = ConfFileSection('test section 2', 'a test section', Action.UPDATE, {'test_key': 'test_value'})
    file = ConfigFile('/test/path', 'test.py', [Action.UPDATE, section_1, section_2])
    assert file.location_dirpath == '/test/path'
    assert file.filename == 'test.py'
    assert type(file.sections[0]) == ConfFileSection
    assert type(file.sections[1]) == ConfFileSection