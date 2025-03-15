from ...SOURCE.modules.cfp_config import ConfFileSection, ConfigFile, Action

def create_conffilesection_test():
    a = Action.UPDATE
    section = ConfFileSection('test section', 'a test section')