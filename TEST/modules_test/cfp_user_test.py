from SOURCE.modules.cfp_user import User
from SOURCE.modules.cfp_errors import CfpTypeError
from pytest import raises
from pathlib import Path

def test_user_failsproperly_test():

    with raises(CfpTypeError):
        user = User('test_handle', 
                    'test@email.com', 
                    'testid', 
                    'test_openid', 
                    'Larry', 
                    'Smith', 
                    'USA', 
                    'New York', 
                    'TestOrg', 
                    'test', 
                    '999', 
                    999, 
                    '888', 
                    888, 
                    '01010101', 
                    '23232323', 
                    123, 
                    'test avatar', 
                    '0123456789')

def test_create_user_test():

    path = Path('/test/path')
    user = User('test_handle', 
                'test@email.com', 
                'testid', 
                'test_openid', 
                'Larry', 
                'Smith', 
                'USA', 
                'New York', 
                'TestOrg', 
                'test', 
                '999', 
                999, 
                '888', 
                888, 
                '01010101', 
                '23232323', 
                123, 
                'test avatar', 
                path)
    assert user.handle == 'test_handle'
    assert user.email == 'test@email.com'
    assert user.vkid == 'testid'
    assert user.openid == 'test_openid'
    assert user.firstname == 'Larry'
    assert user.lastname == 'Smith'
    assert user.country == 'USA'
    assert user.city == 'New York'
    assert user.organization == 'TestOrg'
    assert user.contribution == 'test'