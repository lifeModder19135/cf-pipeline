from SOURCE.modules.cfp_context import IOHandlerBase, IOType, InputHandler, InputType, CfpFile, FileType
import pytest
from SOURCE.modules.cfp_errors import CfpInitializationError, CfpMethodInputError, CfpTypeError, CfpValueError, CfpUserInputError
from pathlib import Path, PosixPath
########################################  ~~~~ IOHandlerBase ~~~~  #####################

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

########################################  ~~~~ InputHandler ~~~~  #####################

def test_create_inputhandler_test():
    hndlr = InputHandler(InputType.INFILE, ['test value 1', 'test value 2'])
    assert hndlr.input_type == InputType.INFILE
    assert hndlr.io_type == IOType.INPUT
    assert hndlr.handler_args[1] == 'test value 2'

def test_create_inputhandler_fails_properly_test():
     with pytest.raises((CfpTypeError, CfpUserInputError)):
         hndlr = InputHandler('wrong type', ['test value 1', 'test value 2'])

########################################  ~~~~ CfpFile ~~~~  #####################

def test_create_cfpfile_test():
    hndlr = InputHandler(InputType.INFILE, ['test value 1', 'test value 2'])
    path = Path('/test/path/testfile.txt')
    file = CfpFile(hndlr, path, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
    assert type(file.handler) == InputHandler
    assert type(file.location_path) == PosixPath
    assert file.filetype == FileType.CFP_INPUTFILE_TEXT_FMT_1
    assert file.is_openable == False

def test_create_inputfilehandler_test():
    hndlr = InputHandler(InputType.INFILE, ['test value 1', 'test value 2'])
    path1 = Path('/test/path/testfile1.txt')
    path2 = Path('/test/path/testfile2.txt')
    file1 = CfpFile(hndlr, path1, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
    file2 = CfpFile(hndlr, path2, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
 
