from setuptools import setup

setup(
    name = 'cf_pipeline', 
    version = '0.0.5', 
    packages = ['cfpipeline', 'cfp_commands', 'cfp_abstract'],
    package_dir = {'cfpipeline': 'SOURCE', 'cfp_commands': 'SOURCE/commands', 'cfp_abstract': 'SOURCE/modules'},
    install_requires = [
        'click',
        'invoke',
        'pytest',
        'requests'
    ],
    entry_points = {'console_scripts': ['cfp=cfpipeline.main:callcfpcommand']}
)
