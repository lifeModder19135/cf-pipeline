import click 
from SOURCE.modules import cfp_context, cfp_config

@click.Group()
def callcfpcommand(Version:bool=False):
    """
    This is the function that is wired to the base cfp command in the terminal, although it is a Group, so it will never be called except to check the version, to get usage info, or in error.
    """
    if Version:
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
    else:
        raise ValueError
    
@
