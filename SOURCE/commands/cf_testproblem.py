#! /usr/bin/env python3

# NAME
#          cf test - test 
#
#
#
#
#
#
#
#

import click
from SOURCE.modules.cfp_context import CfpFile, FileType
from SOURCE.modules.cfp_testcontext import InputParser
from SOURCE.modules.cfp_errors import CfpRuntimeError, CfpUserInputError
from pathlib import Path
from subprocess import run
from os.path import abspath, isdir

@click.command()
@click.argument('solutionfile')
@click.argument('inputfile')
@click.argument('outputfile')
def test_solution(inputfile: str, solutionfile: str, outputfile: str):
    """This will test a codeforces solution against input provided in the format of a cfpin file. For more details about cfpin files, see cfp_context.py."""
    abs = str(abspath('./RESOURCES/test_resources/testinput.py')) 
    output = run('python3 -s ' + abs + ' ' + inputfile + ' | python3 -s ' + solutionfile, capture_output=True, text=True, shell=True)
    exp = InputParser.parse_lines(outputfile)
    lst = []
    st = ''
    for x in output.stdout:
        
        if x == '\n':
            lst.append(str(st))
            st = ''
        else:
            st += x
    if lst == exp:
        print('test passed!\n')
    else:
        print('test failed')
    print('output:')
    print(lst)
    print('\n')
    print('expected:')
    print(exp)
    print(output.stderr)

@click.command()
@click.option('-d', '--dest', default='.')
@click.option('-t', '--type', required=True)
@click.option('-c', '--cases', required=True)
@click.option('-l', '--lines', required=True)
@click.option('-v', '--values', required=True)
def create_fmt_1_file(dest, type, cases, lines, values):
    """
    This command is used for building templates for cfp format 1 files (.cfpin, .cfpout, and .cfpexp files,
    the kind used with cf-testproblem). To use, just execute the command giving values for all of the 
    options. The options describe how you want the file laid out. they are as follows:

    --dest: Where you want the file to be created. Needs to be a valid path. This is
            the only option that is not required. If left out, it defaults to the 
            current directory of the terminal.
    --type: Either input or expected. The kind of file you want to create.
    --cases: The number of cases that you want the file to have
    --lines: The number of lines per case
    --values: The number of space-separated valoes per line
    """
    try:
        abs_path = ''
        if isdir(abspath(dest)) and type == 'input':
            abs_path = str(abspath(dest)) + '/testfile.cfpin'
        elif isdir(abspath(dest)) and type == 'expected':
            abs_path = str(abspath(dest)) + '/testfile.cfpexp'
        elif str(dest).endswith('.cfpin') or str(dest).endswith('.cfpexp'):
            abs_path = str(abspath(dest))
        else:
            raise CfpUserInputError('invalid path supplied to --dest. Must be either the path to a valid directory or a path which includes a filename ending in \'.cfpin\' or \'.cfpexp\' inside a valid directory.')
        with open(abs_path, 'w') as file:
            file.write('!DOCTYPE cfp-fileio-datadoc\n')
            file.write('# This file is still incomplete. To complete it, add your intended values after \n# each empty \'=\' sign in the file.\n')
            file.write('File:\n')
            if type == 'input':
                file.write('    .type = INFILE\n')
                file.write('    .fmt = CFP_INPUTFILE_TEXT_FMT_1\n')
                file.write('Data:\n')
                file.write('    .cases\n')
                file.write('        .numCases = ' + cases + '\n')
                for case in range(int(cases)):
                    file.write('        .case\n')
                    file.write('            .numlines = ' + lines +'\n')
                    for line in range(int(lines)):
                        file.write('            .line\n')
                        for value in range(int(values)):
                            file.write('                .value = \n')
                print('input file successfully created at ' + abs_path + '.')
            elif type == 'expected':
                file.write('    .type = EXPFILE\n')
                file.write('    .fmt = CFP_EXPECTEDFILE_TEXT_FMT_1\n')
                file.write('Data:\n')
                for case in range(int(cases)):
                    file.write('    .case\n')
                    file.write('        .numlines = ' + lines +'\n')
                    for line in range(int(lines)):
                        file.write('        .line\n')
                        for value in range(int(values)):
                            file.write('            .value = \n')
                print('expected file successfully created at ' + abs_path + '.')

    except Exception as e:
        raise e