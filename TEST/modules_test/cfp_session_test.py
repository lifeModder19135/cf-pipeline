from SOURCE.modules.cfp_session import CfSession
from SOURCE.modules.cfp_config import ConfigSection, Configuration


def test_create_cfsession_test():
    sect = ConfigSection('section1', 'section 1', {'key1': 'value 1'})
    conf = Configuration('/test/path', 'test.py', [sect])
    ses = CfSession('uname', 'password', '1234567890', '0987654321', conf)
    assert ses.username == 'uname'
    assert ses.password == 'password'
    assert ses.api_key == '1234567890'
    assert ses.secret == '0987654321'
    assert ses.config == conf