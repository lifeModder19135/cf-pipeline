from SOURCE.modules import cfp_testcontext
from pathlib import Path

def test_input_file_fmt_1_to_input_test(capsys):
    cfp_testcontext.InputParser.input_file_fmt_1_to_input('./RESOURCES/test-resources/testfile.cfpin')
    captured = capsys.readouterr()
    assert captured.out == '2\n3 3\n3 3\n3 3\n3 3\n'
