# from setuptools import setup


setup(
    name = 'Codeforces:_CF_Pipeline',
    version = '',
    package_dirs = {"libcfp_utils": "SOURCE", 'commands': 'SOURCE.commands', 'libcfp_metautils': 'SOURCE.lib.', 'cfp_types': 'SOURCE.modules'},
    install_requires = ['click', 'venv'],
    entry_points = '''
        [console_scripts]
        cfp=main:cli_entry
    '''
)