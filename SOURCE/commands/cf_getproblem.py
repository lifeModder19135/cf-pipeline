import click
import requests
import json
from SOURCE.modules.cfp_problem import Problem

@click.command()
@click.argument('contestid')
@click.argument('index')
def getproblem(contestid: int, index: str):
    """This is a simple command-line program created as an example of how to use this framework. You identify the problem you want by its contest id and its letter index. It returns the available info on that problem. For example, running the command \'cf-getproblem 2093 A\' will return the details for problem A from contest 2093, which happens to be named \"Ideal Generator\"."""
    resp = requests.get('https://codeforces.com/api/problemset.problems')
    jdct = resp.json()
    res = jdct['result']
    probs_list = res['problems']
    problems = []
    for problem in probs_list:
        pr = Problem.from_dict(problem)
        if pr.contest_id == int(contestid) and pr.index == index:
            print(pr)
            break
        else:
            pass
    else:
        print('No results found.')
        problems.append(pr)

@click.command()
@click.argument('a')
@click.argument('b')
def test(a: str, b: str):
    """This is just a test command which prints that it executed successfully with its 2 (required) arguments."""
    print('test command executed with arguments', a, 'and', b, '...')
    