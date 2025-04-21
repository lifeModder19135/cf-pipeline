from SOURCE.modules.cfp_logger import Level, BasicLogger
import pytest
from SOURCE.modules.cfp_errors import CfpTypeError
import os

def test_create_basiclogger_test():
    logger = BasicLogger(Level.DEBUG, 'test.log')
    assert logger.filename == 'test.log'
    assert logger.min_level_printed == Level.DEBUG

def test_basiclogger_fails_correctly_test():
    with pytest.raises(CfpTypeError):
        logger = BasicLogger('DEBUG', 'test.log')

def test_basiclogger_log_method_1_test():
    logger = BasicLogger(Level.DEBUG, 'test.log')
    logger.log('This is a test')
    with open('test.log', 'r') as file:
        assert file.readline() == 'DEBUG:root:This is a test\n'
    path = os.path.join(os.getcwd(), 'test.log')
    os.remove(path)

def test_basiclogger_log_method_2_test():
    logger = BasicLogger(Level.DEBUG, 'test.log')
    logger.log('This is a test', level=Level.WARNING)
    with open('test.log', 'r') as file:
        assert file.readline() == 'WARNING:root:This is a test\n'
    path = os.path.join(os.getcwd(), 'test.log')
    os.remove(path)