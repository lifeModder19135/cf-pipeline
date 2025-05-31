from SOURCE.modules.cfp_config import ConfigSection, Configuration, Action

def test_create_configsection_test():

    section = ConfigSection('test section', 'a test section', {'test_key': 'test_value'})
    assert type(section) == ConfigSection
    assert section.name == 'test section'
    assert section.description == 'a test section'
    assert type(section.values) == dict

def test_update_configsection_test():
    section = ConfigSection('section', 'a test section', {'test_key': 'test_value'})
    section.update({'test_key_2': 'test_value_2'})
    assert section.values['test_key_2'] == 'test_value_2'

def test_create_configfile_test():
    section_1 = ConfigSection('test section 1', 'a test section', {'test_key': 'test_value'})
    section_2 = ConfigSection('test section 2', 'a test section', {'test_key': 'test_value'})
    file = Configuration('/test/path', 'test.py', [section_1, section_2])
    assert file.location_dirpath == '/test/path'
    assert file.filename == 'test.py'
    assert type(file.sections[0]) == ConfigSection
    assert type(file.sections[1]) == ConfigSection