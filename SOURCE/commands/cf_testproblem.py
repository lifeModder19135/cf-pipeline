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
from SOURCE.modules.cfp_context import CfpFile
from pathlib import Path

@click.command()
@click.argument('solutionfile')
@click.argument('inputfile')
def test_solution(inputfile: str, solutionfile: str):
    if_path = Path(inputfile)
    sf_path = Path(solutionfile)
