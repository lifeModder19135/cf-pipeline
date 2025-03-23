from SOURCE.modules.cfp_context import IOHandlerBase, IOType


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

def test_create_inputhandler_test():
    pass