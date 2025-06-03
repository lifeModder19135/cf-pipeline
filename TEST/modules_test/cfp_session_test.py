from SOURCE.modules.cfp_session import CfSession
from SOURCE.modules.cfp_config import ConfigSection, Configuration
import os


def get_slash():
    if os.name == 'posix' or os.name == 'java':
        return '/'
    else:
        return '\\'

def test_create_cfsession_test():
    slash = get_slash()
    dirpath = os.path.abspath('RESOURCES' + slash + 'test_resources')
    conf = Configuration(dirpath, 'test_config_file_2', [])
    ses = CfSession('uname', 'password', '1234567890', '0987654321', conf)
    assert ses.username == 'uname'
    assert ses.password == 'password'
    assert ses.api_key == '1234567890'
    assert ses.secret == '0987654321'
    assert ses.config == conf
    fullpath = dirpath + slash + 'test_config_file_2'
    if os.path.exists(fullpath):
        os.remove(fullpath)