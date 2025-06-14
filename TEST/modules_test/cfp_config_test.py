from SOURCE.modules.cfp_config import ConfigSection, Configuration, Action
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

def test_configuration_add_section_new_obj_test():

    # create Configuration obj and config file
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_3'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # use method to add section
    updated = conf.add_section('new_section', 'a new config section', {'new_key1': 'new_val1', 'new_key2': 'new_val2'})

    # assert that section was added to both sections and file
    assert updated == True
    assert len(conf.sections) == 3
    with open(fullpath, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 9

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_section_existing_obj_test():

    # create Configuration obj and config file
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_3'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # create new ConfigSection obj
    sec3 = ConfigSection('new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})

    # use method to add new section
    updated = conf.add_section(section_obj=sec3)

    # assert that section was added to both sections and file
    assert updated == True
    assert len(conf.sections) == 3
    with open(fullpath, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 9

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_section_wrong_params_test():

    # create Configuration obj and config file
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_3'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # create new ConfigSection obj
    sec3 = ConfigSection('new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})

    # try method with invalid params; assert failure
    with pytest.raises(CfpMethodInputError):
        test = conf.add_section(section_name='name', section_obj=sec3)

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_remove_section_test():

    # create config object
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_2'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])
    
    # use method to remove section
    removed = conf.remove_section('section_1')

    #assert section was removed from both sections and file
    assert removed == True
    assert len(conf.sections) == 1
    with open(fullpath) as file:
        lines = file.readlines()
        assert len(lines) == 3

       # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_update_sections_test():

    # create config object
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_2'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # add extra sections (to object only, not file, should be deleted on sync)
    sec3 = ConfigSection('new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})
    sec4 = ConfigSection('second_new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})
    conf.sections = [Action.UPDATE, [sec3, sec4]]

    # write new sections to config file
    with open(fullpath, 'a') as file:
        file.write('[[new_file_section]]\n')
        file.write('new_key = new value\n')
        file.write('other_key = other value\n')
        file.write('third_key = third value\n')

    # run method to sync
    conf.update_sections()

    # assert that the two are in sync
    assert len(conf.sections) == 3
    assert conf.sections[2].name == 'new_file_section'

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_update_conffile_test():
    
    # create config object
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_4'
    fullpath = dirpath + slash + filename
    if os.path.exists(fullpath):
        os.remove(fullpath)
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # add extra sections (to object only, not file, should be deleted on sync)
    sec3 = ConfigSection('new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})
    sec4 = ConfigSection('second_new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})
    conf.sections = [Action.UPDATE, [sec3, sec4]]

    # write new section to config file
    with open(fullpath, 'a') as file:
        file.write('[[new_file_section]]\n')
        file.write('new_key = new value\n')
        file.write('other_key = other value\n')
        file.write('third_key = third value\n') 

    # run method to sync conf file
    synced = conf.update_conffile()

    # assert that sec3 and sec4 are added to conf file and that file-only section is deleted
    assert synced == True
    with open(fullpath, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 12
        assert lines[6] == '[[new_obj_section]]\n'

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_section_from_sections_to_config_file_test():

    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_3'
    fullpath = dirpath + slash + filename

    # make sure config file doesn't esist
    if os.path.exists(fullpath):
        os.remove(fullpath)

    # create Configuration obj and config file
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # add section to Configuration only, not file
    sec3 = ConfigSection('new_obj_section', 'a new section', {'val_1': 'new', 'val2': 'section'})
    conf.sections = [Action.UPDATE, [sec3]]

    # use method to add sec3 to config file
    added = conf._Configuration__add_section_from_sections_to_config_file('new_obj_section')

    # assert that section is added to file
    with open(fullpath, 'r') as file:
        fi = file.readlines()
        assert len(fi) == 9

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_add_config_file_section_to_sections_test():
    pass

def test_configuration_remove_section_from_sections_test():
    pass

def test_configuration_remove_section_from_conf_file_test():

    # create Configuration obj and config file
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    filename = 'test_config_file_2'
    fullpath = dirpath + slash + filename
    sec1 = ConfigSection('section_1', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    sec2 = ConfigSection('section_2', 'a config section', {'key1': 'val1', 'key2': 'val2'})
    conf = Configuration(dirpath, filename, [sec1, sec2])

    # run tested method on first section
    deleted = conf._Configuration__remove_section_from_conf_file('section_1')

    # assert that method ran successfully and section was deleted
    assert deleted == True
    with open(fullpath, 'r') as file:
        assert file.readline() == '[[section_2]]\n'

    # cleanup
    if os.path.exists(fullpath):
        os.remove(fullpath)

def test_configuration_write_dict_to_conf_file_test():
    pass

def test_configuration_write_section_to_conf_file_test():
    pass



