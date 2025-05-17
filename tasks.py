from invoke import task
from subprocess import run

@task
def tst(ctx):
    print('invoke works!')

@task
def act(ctx):
    ctx.run('. venv/bin/activate')

@task
def instpt(ctx):
    ctx.run('pip install pytest')

@task
def runpt(ctx):
    ctx.run('. venv/bin/activate && python3 -m pytest')

@task
def sphinxrbld(ctx):
    
    ctx.run('rm -rf DOCS/cf-pipeline.rst')
    ctx.run('rm -rf DOCS/cf-pipeline.SOURCE.rst')
    ctx.run('rm -rf DOCS/cf-pipeline.SOURCE.commands.rst')
    ctx.run('rm -rf DOCS/cf-pipeline.SOURCE.lib.rst')
    ctx.run('rm -rf DOCS/cf-pipeline.SOURCE.modules.rst')
    ctx.run('rm -rf DOCS/modules.rst')
    ctx.run('rm -rf DOCS/_build/*')
    ctx.run('cd DOCS && sphinx-apidoc -o . ..')
    ctx.run('cd DOCS && make html')

@task
def build(ctx):
    ctx.run('rm -rf dist/*')
    ctx.run('python3 -m build')

@task(build)
def deploy(ctx):
    ctx.run('python3 -m twine upload dist/*')