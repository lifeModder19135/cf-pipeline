import os, subprocess

class simple_tester(lang,input_file,source_file):
    
    def setup_pipes():
        ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)

