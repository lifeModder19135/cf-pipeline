import click 
from SOURCE.modules import cfp_context, cfp_config

@click.Group()
@click.option('-v', '-V', '--version', is_flag=True, default=False)
@click.option('-c', '-C', '--contribute', is_flag=True, default=False)
def callcfpcommand(version, contribute):
    """
    This is the function that is wired to the base cfp command in the terminal, although it is a Group, so it will never be called except to check the version, to get usage info, or in error.
    """
    if version and contribute:
        click.echo('The \'--version\' and \'contribute\' options are mutually exclusive. You can only use one at a time.')
    if version:
        click.echo("""
            ~~~~~~ CfPipeline -- V-0.0.5  ~~~~~~~~

            Version:
                Major:       0
                Minor:       0
                itty-bitty:  5
                SDLC_stage: 
                    tag:     early_devel
                    desc:    Not "complete" enough even for alpha yet
                Codename:    "AlmostAlpha"
        """)
        return '0'
    elif contribute:
        click.echo("""
                   Looking for a project to contribute to? This one is looking for 
                   developers with big ideas. have an idea for a command that would
                   improve your competitive programming workflow. Build it, add it in 
                   a github pull request, and it will likely become part of the 
                   cf-pipeline package. 

                   The cf-pipeline github repo can be found at 
                   https://github.com/lifeModder19135/cf-pipeline.
                   All of the source code is available inside the 'SOURCE' directory.
                   This is a fairly large project with a lot of 'stubs' or functions that are
                   yet to be built. These are opportunities to add your mark to the project.

                   This project, for me, has been a blast to work on, and so I want to share 
                   the opportunity with others!

                   For more details on contributing, check out RESOURCES/README.rst in the repo, or 
                   visit https://github.com/lifeModder19135/cf-pipeline/blob/dev-master/RESOURCES/README.rst.
                   This document is currently out of date in some areas, but should be updated soon.

        """)
    else:
        click.echo('Welcome to cf-pipeline!\nTIP: Call this command with \'--help\' option for a list of available options.')
