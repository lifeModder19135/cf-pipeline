from SOURCE.modules.cfp_config import ConfigSection, Configuration
from SOURCE.modules.cfp_errors import CfpMethodInputError
import os
import pytest

def get_slash():
    if os.name == 'posix' or os.name == 'java':
        return '/'
    else:
        return '\\'

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

def test_create_configuration_test():
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    fullpath = dirpath + slash + 'test_config_file_2'
    if os.path.exists(fullpath):
        os.remove(fullpath)
    section_1 = ConfigSection('test_section_1', 'a test section', {'key1': 'value 1', 'key2': 'value 2'})
    section_2 = ConfigSection('test_section_2', 'a test section', {'key1': 'value 1', 'key2': 'value 2'})
    conf = Configuration(dirpath, 'test_config_file_2', [section_1, section_2])
    assert conf.location_dirpath == dirpath
    assert conf.filename == 'test_config_file_2'
    assert type(conf.sections[0]) == ConfigSection
    assert type(conf.sections[1]) == ConfigSection
    with open(fullpath, 'r') as file:
        assert file.readline() == '[[test_section_1]]\n'
        assert file.readline() == 'key1 = value 1\n'
        assert file.readline() == 'key2 = value 2\n'
        assert file.readline() == '[[test_section_2]]\n'
        assert file.readline() == 'key1 = value 1\n'
        assert file.readline() == 'key2 = value 2\n'
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration__get_slash_type_linux_test(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, 'name', 'posix')
    slash1 = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash1 + 'test_resources')
    conf = Configuration(dirpath, 'test_config_file_2', [])
    slash = conf._Configuration__get_slash_type()
    assert slash == '/'
    rempath = 'RESOURCES\\test_resources\\test_config_file_2'
    if os.path.exists(rempath):
        os.remove(rempath)


def test_configuration__get_slash_type_windows_test(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, 'name', 'nt')
    slash1 = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash1 + 'test_resources')
    conf = Configuration(dirpath, 'test_config_file_2', [])
    slash = conf._Configuration__get_slash_type()
    assert slash == '\\'
    rempath = 'RESOURCES\\test_resources\\test_config_file_2'
    if os.path.exists(rempath):
        os.remove(rempath)

def test_configuration_create_config_file_doesnt_exist_test():
    slash = get_slash()
    fullpath = os.path.abspath('RESOURCES' + slash + 'test_resources' + slash + 'test_config_file_2')
    if os.path.exists(fullpath):
        os.remove(fullpath)
    section_1 = ConfigSection('test section 1', 'a test section', {'test_key': 'test_value'})
    section_2 = ConfigSection('test section 2', 'a test section', {'test_key': 'test_value'})
    conf = Configuration(os.path.abspath('RESOURCES' + slash + 'test_resources'), 'test_config_file_2', [section_1, section_2])
    exists = conf.create_config_file()
    assert exists == True
    assert os.path.exists(fullpath)
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_create_config_file_exists_test():
    slash = get_slash()
    fullpath = os.path.abspath('RESOURCES' + slash + 'test_resources' + slash + 'test_config_file_2')
    if not os.path.exists(fullpath):
        with open(fullpath, 'x'):
            pass
    conf = Configuration(os.path.abspath('RESOURCES' + slash + 'test_resources'), 'test_config_file_2', [])
    exists = conf.create_config_file()
    assert exists == True
    assert os.path.exists(fullpath)
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_section_to_config_file_test():
    slash = get_slash()
    fullpath = os.path.abspath('RESOURCES' + slash + 'test_resources' + slash + 'test_config_file_2')
    if not os.path.exists(fullpath):
        with open(fullpath, 'x'):
            pass
    secname = 'test_section'
    valslist = ['key1 = val1', 'key2 = val2']
    conf = Configuration(os.path.abspath('RESOURCES/test_resources/'), 'test_config_file_2', [])
    written = conf.add_section_to_config_file(secname, valslist)
    assert written == True
    with open(fullpath, 'r') as file:
        assert file.readline() == '[[test_section]]\n'
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_section_to_config_file_fails_correctly_test():
    slash = get_slash()
    fullpath = os.path.abspath('RESOURCES' + slash + 'test_resources' + slash + 'test_config_file_2')
    if not os.path.exists(fullpath):
        with open(fullpath, 'x'):
            pass
    secname = 'test_section'
    valslist = ['key1 = val1', 'key2 = val2', 'bad value']
    conf = Configuration(os.path.abspath('RESOURCES/test_resources/'), 'test_config_file_2', [])
    with pytest.raises(CfpMethodInputError):
        written = conf.add_section_to_config_file(secname, valslist)
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_get_section_from_config_file_test():
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    fullpath = dirpath + slash + 'test_config_file_2'
    with open(fullpath, 'w') as file:
        file.write('[[test_section]]\n')
        file.write('key1 = value 1\n')
        file.write('key2 = value 2\n')
    conf = Configuration(dirpath, 'test_config_file_2', [])
    sect = conf.get_section_from_config_file(section_name='test_section', description='desc')
    assert sect.name == 'test_section'
    assert sect.description == 'desc'
    assert sect.values['key1'] == 'value 1'
    assert sect.values['key2'] == 'value 2'
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_get_section_names_from_conffile_test():
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    fullpath = dirpath + slash + 'test_config_file_2'
    with open(fullpath, 'w') as file:
        file.write('[[test_section_1]]\n')
        file.write('key1 = value 1\n')
        file.write('key2 = value 2\n')
        file.write('[[test_section_2]]\n')
        file.write('key1 = value 1\n')
        file.write('key2 = value 2\n')
        file.write('[[test_section_3]]\n')
        file.write('key1 = value 1\n')
        file.write('key2 = value 2\n')
    conf = Configuration(dirpath, 'test_config_file_2', [])
    secnames = conf.get_section_names_from_conffile()
    assert secnames[0] == 'test_section_1'
    assert secnames[1] == 'test_section_2'
    assert secnames[2] == 'test_section_3'
    if os.path.exists(fullpath):
        os.remove(fullpath)

