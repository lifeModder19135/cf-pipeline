<<<<<<< HEAD
from setuptools import setup, find_packages

setup(
    name = 'cfpipeline', 
    version = '0.0.1', 
=======
from setuptools import setup

setup(
    name = 'cf_pipeline', 
    version = '0.0.5', 
>>>>>>> dev-master
    packages = ['cfpipeline', 'cfp_commands', 'cfp_abstract'],
    package_dir = {'cfpipeline': 'SOURCE', 'cfp_commands': 'SOURCE/commands', 'cfp_abstract': 'SOURCE/modules'},
    install_requires = [
        'click',
        'poetry',
        'invoke',
        'pytest',
        'ward'
    ],
<<<<<<< HEAD
    entry_points = '''
        [console_scripts]
        cfp=cfpipeline 
    '''
    )
=======
    entry_points = {'console_scripts': ['cfp=cfpipeline.main:callcfpcommand']
>>>>>>> dev-master
