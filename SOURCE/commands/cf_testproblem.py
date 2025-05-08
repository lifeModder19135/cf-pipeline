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
from pathlib import Path
from subprocess import run
from os.path import abspath

@click.command()
@click.argument('solutionfile')
@click.argument('inputfile')
@click.argument('outputfile')
def test_solution_old(inputfile: str, solutionfile: str, outputfile: str):
    """This will test a codeforces solution against input provided in the format of a cfpin file. For more details about cfpin files, see cfp_context.py."""
    abs = str(abspath('./RESOURCES/test_resources/testinput.py'))
    input = run('python3 -s ' + abs + ' ' + inputfile, capture_output=True, text=True, shell=True) 
    output = run('python3 -s ' + solutionfile + ' | testoutput.py ' + outputfile, stdin=input.stdout, capture_output=True, text=True, shell=True)
    exp = InputParser.parse_lines(outputfile)
    if output.stdout == exp:
        print('test passed!\n')
    else:
        print('test failed')
    print('output:')
    print(output.stdout)
    print('\n')
    print('expected:')
    print(exp)

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