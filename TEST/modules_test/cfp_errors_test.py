from SOURCE.modules.cfp_errors import CfpInitializationError, CfpIOError, CfpConfigurationError, CfpMethodInputError, CfpUserInputError, CfpTypeError, CfpValueError, CfpPermissionDeniedError, CfpRuntimeError, CfpOverwriteNotAllowedError, CfpNotExecutableError, CfpTimeoutError
import pytest

def test_cfpiniterror_raises_test():
    with pytest.raises(CfpInitializationError):
        raise CfpInitializationError('test')
    
def test_cfpioerror_raises_test():
    with pytest.raises(CfpIOError):
        raise CfpIOError('test')

def test_cfpconfigurationerror_raises_test():
    with pytest.raises(CfpConfigurationError):
        raise CfpConfigurationError('test')
    
def test_cfpmethodinputerror_raises_test():
    with pytest.raises(CfpMethodInputError):
        raise CfpMethodInputError('test')
    
def test_cfpuserinputerror_raises_test():
    with pytest.raises(CfpUserInputError):
        raise CfpUserInputError('test')
    
def test_cfptypeerror_raises_test():
    with pytest.raises(CfpTypeError):
        raise CfpTypeError('test')

def test_cfpvalueerror_raises_test():
    with pytest.raises(CfpValueError):
        raise CfpValueError('test')
    
def test_cfppermissiondeniederror_raises_test():
    with pytest.raises(CfpPermissionDeniedError):
        raise CfpPermissionDeniedError('test')
    
def test_cfpruntimeerror_raises_test():
    with pytest.raises(CfpRuntimeError):
        raise CfpRuntimeError('test')
        
def test_cfpoverwritenotallowederror_raises_test():
    with pytest.raises(CfpOverwriteNotAllowedError):
        raise CfpOverwriteNotAllowedError('test')
    
def test_cfpnotexecutableerror_raises_test():
    with pytest.raises(CfpNotExecutableError):
        raise CfpNotExecutableError('test')
        
def test_cfptimeouterror_raises_test():
    with pytest.raises(CfpTimeoutError):
        raise CfpTimeoutError('test')