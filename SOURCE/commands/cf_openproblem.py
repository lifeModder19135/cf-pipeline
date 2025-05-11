import webbrowser
import click

@click.command()
@click.argument('contestid', required=False, default=None)
@click.argument('index', required=False, default=None)
@click.option('-a', '--all', is_flag=True, default=False)
def open_problem(contestid, index, all):
    if all and contestid == None and index == None:
        webbrowser.open('https://codeforces.com/problemset')
    elif not all and contestid != None and index != None:
        url = 'https://codeforces.com/problemset/problem/' + contestid + '/' + index
        webbrowser.open(url)
    else:
        click.echo('USAGE ERROR: this command can only be invoked with either 2 arguments (CONTESTID and INDEX) or with \'--all\' or \'-a\' and no arguments.')