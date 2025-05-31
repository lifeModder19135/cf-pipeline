from SOURCE.modules.cfp_pathutils import PathTool, CfpUrl
import os


def test_pathtool_slashpath_remove_outermost_prefix_linux_abs_test():
    realos = os.name
    os.name = 'posix'
    path = '/home/user/downloads'
    new_path = PathTool.slashpath_remove_outermost_prefix(path)
    assert new_path == 'user/downloads'
    os.name = realos

def test_pathtool_slashpath_remove_outermost_prefix_linux_rel_test():
    realos = os.name
    os.name = 'posix'
    path = 'user/downloads/download1'
    new_path = PathTool.slashpath_remove_outermost_prefix(path)
    assert new_path == 'downloads/download1'
    os.name = realos

def test_pathtool_slashpath_remove_outermost_prefix_windows_abs_test():
    realos = os.name
    os.name = 'windows'
    path = r'C:\users\user\home'
    new_path = PathTool.slashpath_remove_outermost_prefix(path)
    assert new_path == r'user\home'
    os.name = realos

def test_pathtool_slashpath_remove_outermost_prefix_windows_rel_test():
    realos = os.name
    os.name = 'windows'
    path = r'users\user\home'
    new_path = PathTool.slashpath_remove_outermost_prefix(path)
    assert new_path == r'user\home'
    os.name = realos

def test_slashpath_separate_filename_from_pathprefix_linux_file_test():
    realos = os.name
    os.name = 'posix'
    path = '/home/user/download.file'
    path_list = PathTool.slashpath_separate_filename_from_pathprefix(path)
    assert path_list[0] == '/home/user'
    assert path_list[1] == '/'
    assert path_list[2] == 'download.file'
    os.name = realos

def test_slashpath_separate_filename_from_pathprefix_linux_dir_test():
    realos = os.name
    os.name = 'posix'
    path = '/home/user/downloads/'
    path_list = PathTool.slashpath_separate_filename_from_pathprefix(path)
    assert path_list[0] == '/home/user'
    assert path_list[1] == '/'
    assert path_list[2] == 'downloads'
    os.name = realos

def test_slashpath_separate_filename_from_pathprefix_windows_dir_test():
    realos = os.name
    os.name = 'windows'
    path = 'C:\\home\\user\\downloads\\'
    path_list = PathTool.slashpath_separate_filename_from_pathprefix(path)
    assert path_list[0] == 'C:\\home\\user'
    assert path_list[1] == '\\'
    assert path_list[2] == 'downloads'
    os.name = realos

def test_slashpath_separate_filename_from_pathprefix_windows_file_test():
    realos = os.name
    os.name = 'windows'
    path = 'C:\\home\\user\\download1.exe'
    path_list = PathTool.slashpath_separate_filename_from_pathprefix(path)
    assert path_list[0] == 'C:\\home\\user'
    assert path_list[1] == '\\'
    assert path_list[2] == 'download1.exe'
    os.name = realos

