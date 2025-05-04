import click 
from SOURCE.modules import cfp_context, cfp_config

@click.command()
@click.option('-v', '-V', '--version', is_flag=True, default=False)
@click.option('-c', '-C', '--contribute', is_flag=True, default=False)
@click.option('-u', '-U', '--usage', is_flag=True, default=False)
def callcfpcommand(version, contribute, usage):
    """
    This command is meant for new users to cf-pipeline. using the various options, you can get useful info on the version, usage info, and even info on contributing to the project.
    """
    if version and contribute or version and usage or contribute and usage:
        click.echo('The \'--version\', \'--usage\', and \'--contribute\' options are mutually exclusive. You can only use one at a time.')
    elif version:
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
    elif usage:
        click.echo("""
        This package is divided into two parts: the commands and the framework.
        The commands come ready to use out of the box. There are only a few at the moment,
        but more are coming soon. The commands perform actions that are useful to competitive
        programmers.
                   
        The commands are nice by themselves, but are not what makes this package unique. The
        framework is provided so that you can easily make commands of your own! Have an idea 
        for a terminal command that would improve your competitive programming workflow? With 
        cf-pipeline, these ideas can easily become a reality. 

        To start building commands, you need two things: a basic understanding of object-oriented 
        programming in Python and the same for the python click library. To get started with 
        click, visit https://click.palletsprojects.com/en/stable/. The click library is very
        fun and easy to use. Basically, you write a python function and turn it into a command 
        line program with a single decorator! I promise you will enjoy it.

        To see what the framework has to offer, check out 
        https://github.com/lifeModder19135/cf-pipeline/tree/dev-master/SOURCE/modules.
        There you will find the framework itself. It currently contains ten(ish) modules 
        designed to be used to assist in building your command functions. Some are just
        python classes mapped to the codeforces API objects. Others contain classes used
        for creating configs, building out contexts, and more. I purposefully chocked
        the modules full of comments to make them easier to understand.

        If you build a module that you think will be useful to others, consider adding it 
        to the package. Just pull the project via GitHub, add your script inside the 
        SOURCE/commands/ directory, add a line to the [project.scripts] section of the 
        pyproject.toml file at the top level of the project in the following format:
             {command-name} = "SOURCE.commands.{script-name}:{function-name}"
        and send me a pull request. If it works and is useful, chances are that I'll
        probably accept it. If it does not work, but I can tell what you are trying to 
        do, I'll try to fix it for you.

        Hopefully, cf-pipeline will bring you as much fun as it has brought me. Thank 
        you for checking it out. (a git joke)
        """)
    else:
        click.echo('Welcome to cf-pipeline!\nTIP: Call this command with \'--help\' option for a list of available options.')
