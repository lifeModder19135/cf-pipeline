import os, subprocess
from SOURCE.modules.cfp_context import CfpFile

class simple_tester():
    
    def setup_pipes():
        ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)

class InputParser:

    def parse_input_file(inputfile: CfpFile):
        path = inputfile.location_path
        with open(path, 'r') as file:
            output = {'file_info': [], 'data': []}
            for line in file.readlines:
                if line.lstrip().startswith('File:'):
                    pass
                elif line.lstrip().startswith('Data:'):
                    pass