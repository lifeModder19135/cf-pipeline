import os, subprocess

class simple_tester():
    
    def setup_pipes():
        ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)

