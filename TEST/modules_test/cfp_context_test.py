from SOURCE.modules.cfp_context import IOHandlerBase


def test_create_iohandlerbase_test():
    base = IOHandlerBase(test_key='test value')
    assert base.handler_args[0] == 'test value'
