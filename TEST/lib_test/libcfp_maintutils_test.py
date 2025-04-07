from SOURCE.lib.libcfp_maintutils import create_mock_conf_file, delete_nock_conf_file, OptionChoice
import os

def test_create_mock_conf_file_test():
    create_mock_conf_file('testdir', 'testfile.txt')
    line = None
    path = None
    if os.name == 'posix' or os.name == 'java':
        path = 'testdir/testfile.txt'
    elif os.name == 'nt':
        path = 'testdir\\testfile.txt'
    with open(path, 'r') as f:
        line = f.readlines()[0]
    assert line == '[[SECTION_1]]\n'
    delete_nock_conf_file('testdir')

def test_create_optionchoice_test():
    oc = OptionChoice(['choice 1', 'choice 2'])