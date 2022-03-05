from setuptools import setup, find_packages

setup(
    name = 'cfpipeline', 
    version = '0.0.1', 
    packages = ['cfpipeline', 'cfp_commands', 'cfp_abstract'],
    package_dir = {'cfpipeline': 'SOURCE', 'cfp_commands': 'SOURCE/commands', 'cfp_abstract': 'SOURCE/modules'},
    install_requires = [
        'click',
        'poetry',
        'invoke',
        'pytest',
        'ward'
    ],
    entry_points = '''
        [console_scripts]
        cfp=cfpipeline 
    '''
    )
