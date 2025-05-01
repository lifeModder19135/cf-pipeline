from SOURCE.modules import cfp_testcontext
from pathlib import Path

def test_input_file_fmt_1_to_input_test(capsys):
    cfp_testcontext.InputParser.input_file_fmt_1_to_input('/home/ntolb/CODING_PROJECTS/python_workspaces/0-vscode_ws/cf-pipeline/TEST/modules_test/testfile.cfpin')
    captured = capsys.readouterr()
    assert captured.out == '2\n3 3 \n3 3 \n3 3 \n3 3 '

def test_fake_test():
    cleanline = 'val = 2'
    res = str(cleanline.split(' ')[2])
    assert res == '2'