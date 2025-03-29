from SOURCE.modules.cfp_context import IOHandlerBase, IOType, InputHandler, InputType, CfpFile, FileType, InputFileHandler, OutputHandler, OutputType, InputCommandString, Program, CmdArg, CmdArgString, CmdArgList, CommandLine, Task, ShellProgram, Job, BaseRunner, CfpRunner, Context, CfpShellBasedTestContext, DynamicStrRunnerContext, CfpShellContext, Separator
import pytest
from SOURCE.modules.cfp_errors import CfpInitializationError, CfpMethodInputError, CfpTypeError, CfpValueError, CfpUserInputError, CfpOverwriteNotAllowedError
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
    path = Path('/test/path/testfile.txt')
    file = CfpFile(path, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
    assert type(file.location_path) == PosixPath
    assert file.filetype == FileType.CFP_INPUTFILE_TEXT_FMT_1
    assert file.is_openable == False

########################################  ~~~~ InputFileHandler ~~~~  #####################

def test_create_inputfilehandler_test():
    path1 = Path('/test/path/testfile1.txt')
    path2 = Path('/test/path/testfile2.txt')
    file1 = CfpFile(path1, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
    file2 = CfpFile(path2, FileType.CFP_INPUTFILE_TEXT_FMT_1, 100)
    hndlr = InputFileHandler([file1, file2], ['arg 1', 'arg 2'])
    assert hndlr.current_file == file1
    assert hndlr.files_previously_handled == []
    assert hndlr.files_on_deck[0] == file2
 
 ########################################  ~~~~ OutputHandler ~~~~  #####################

def test_create_outputhandler_test():
    hndlr = OutputHandler(OutputType.OUTFILE, ['test value 1', 'test value 2'])
    assert hndlr.handler_args[1] == 'test value 2'
    assert hndlr.output_type == OutputType.OUTFILE
    assert hndlr.io_type == IOType.OUTPUT

def test_outputhandler_iotype_changeability_test():
    hndlr = OutputHandler(OutputType.OUTFILE, ['test value 1', 'test value 2'])
    with pytest.raises(CfpOverwriteNotAllowedError):
        hndlr.io_type = IOType.INPUT

 ########################################  ~~~~ InputCommandString ~~~~  #####################

def test_create_commandstring_test():
    cmdstr = InputCommandString('test -command', 'bash')
    assert cmdstr.command == 'test -command'
    assert cmdstr.primary_shellchoice == 'bash'

 ########################################  ~~~~ Program ~~~~  ################################

def test_create_program_test():
    pa = Path('/test/path.py')
    pr = Program(pa, 'posix', 'test user')
    assert type(pr.fullpath) == PosixPath
    assert pr.invoked_by == 'test user'
    assert pr.operating_system == 'posix'

def test_program_tostring_test():
    pa = Path('/test/path.py')
    pr = Program(pa, 'posix', 'test user')
    assert pr.tostring() == '/test/path.py'

 ########################################  ~~~~ CmdArg ~~~~  ################################

def test_create_cmdarg_test():
    arg = CmdArg('testarg')
    assert arg.argument == 'testarg'

 ########################################  ~~~~ CmdArgString ~~~~  ################################

def test_create_cmdargstring_test():
    assert CmdArgString('-option') == str('-option')

 ########################################  ~~~~ CmdArgList ~~~~  ################################

def test_create_cmdargList_fromcmdarg_test():
    arg = CmdArg('-testarg')
    cmdls = CmdArgList(arg)
    assert cmdls.args[0].argument == '-testarg'

def test_create_cmdargList_fromlist_test():
    ls = ['argument', '-option']
    cmdls = CmdArgList(ls)
    assert cmdls.args[1].argument == '-option'

def test_create_cmdargList_fromtuple_test():
    t = ('argument', '-option')
    cmdls = CmdArgList(t)
    assert cmdls.args[1].argument == '-option'

def test_create_cmdargList_fromint_test():
    cmdls = CmdArgList(1)
    assert cmdls.args[0].argument == '1'

def test_create_cmdargList_fromstring_test():
    cmdls = CmdArgList('-option')
    assert cmdls.args[0].argument == '-option'

def test_cmdarglist_tostring_test():
    ls = ['argument', '-option']
    cal = CmdArgList(ls)
    str = cal.tostring() == 'argument -option'

 ########################################  ~~~~ CommandLine ~~~~  ################################

def test_create_commandline_test():
    pr = Program('/test/program.py', 'linux', 'test caller')
    cal = CmdArgList('test')
    cl = CommandLine(pr, cal)
    assert type(cl.args) == CmdArgList
    assert type(cl.args.args[0]) == CmdArg
    assert cl.args.args[0].argument == 'test'
    assert type(cl.executable) == Program

def test_commandline_tostring_test():
    pr = Program('/test/program', 'linux', 'test caller')
    cal = CmdArgList('test')
    cl = CommandLine(pr, cal)
    str = cl.tostring()
    assert str == '/test/program test'

 ########################################  ~~~~ Task ~~~~  ################################

def test_create_task_test():
    pr1 = Program('/test/program1.py', 'linux', 'test caller')
    cal1 = CmdArgList('test')
    cl1 = CommandLine(pr1, cal1)
    pr2 = Program('/test/program2.py', 'linux', 'test caller')
    cal2 = CmdArgList('test')
    cl2 = CommandLine(pr2, cal2)
    s1 = Separator.AMPERSANDS
    s2 = Separator.SEMICOLON
    l1 = [cl1, cl2]
    l2 = [s1, s2]
    tsk = Task(l1, l2)
    assert type(tsk.content[1]) == CommandLine
    assert type(tsk.separators[1]) == Separator