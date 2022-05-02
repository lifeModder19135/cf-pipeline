import os, subprocess
from .cfp_context import CfpFile, CfpRunner

class simple_tester(CfpRunner):
    
    def setup_pipes(lang,input_file:CfpFile,source_file:CfpFile):
        ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)

