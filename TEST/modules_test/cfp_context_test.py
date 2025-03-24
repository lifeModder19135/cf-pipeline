from SOURCE.modules.cfp_context import IOHandlerBase, IOType, InputHandler, InputType
import pytest
from SOURCE.modules.cfp_errors import CfpInitializationError, CfpMethodInputError, CfpTypeError, CfpValueError, CfpUserInputError


def test_create_iohandlerbase_test():
    base = IOHandlerBase(['test value 1', 'test value 2'], IOType.INPUT)
    assert base.io_type == IOType.INPUT
    assert type(base.handler_args) == list
    assert base.handler_args[0] == 'test value 1'

def test_create_iohandlerbase_withstring_test():
    base = IOHandlerBase(['test value 1', 'test value 2'], 'i')
    assert base.io_type == IOType.INPUT
    assert type(base.handler_args) == list
    assert base.handler_args[0] == 'test value 1'

def test_create_iohandlerbase_fails_properly_test():
    with pytest.raises((CfpValueError, CfpUserInputError)):
        base = IOHandlerBase(['test value 1', 'test value 2'])
    with pytest.raises((CfpValueError, CfpUserInputError)):
        base = IOHandlerBase(['test value 1', 'test value 2'], 'bad input')
    with pytest.raises((CfpValueError, CfpUserInputError)) as e:
        base = IOHandlerBase(['test value 1', 'test value 2'], 14)
    # assert str(e.value) == 'The value provided for io_type must be of type string or IOType.'

def test_create_inputhandler_test():
    hndlr = InputHandler(InputType.INFILE, ['test value 1', 'test value 2'])
    assert hndlr.input_type == InputType.INFILE
    assert hndlr.io_type == IOType.INPUT
    assert hndlr.handler_args[1] == 'test value 2'