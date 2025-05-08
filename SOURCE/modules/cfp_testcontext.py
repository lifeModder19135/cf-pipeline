import os, subprocess
from SOURCE.modules.cfp_context import CfpFile
from SOURCE.modules.cfp_errors import CfpRuntimeError
from pathlib import Path
import subprocess
from subprocess import run

class simple_tester():
    
    def setup_pipes():
        ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)
        #TODO finish me

class InputParser:

    def parse_input_file(inputfile: CfpFile):
        path = inputfile.location_path
        with open(path, 'r') as file:
            output = {'file_info': [], 'data': []}
            for line in file:
                if line.lstrip().startswith('File:'):
                    pass
                elif line.lstrip().startswith('Data:'):
                    pass

    @staticmethod
    def parse_lines(inputfile: str) -> list[str]:
        try:
            with open(inputfile, 'r') as file:
                output_lines = []
                current_case = []
                num_cases = 0
                inside_line = False
                for line in file:
                    match line.strip().split('='):
                        case '.numCases ', value:
                            num_cases = int(value.strip())
                            output_lines.append(str(num_cases))
                        case '.line', *_:
                            if current_case:
                                output_lines.append(' '.join(current_case))
                                current_case = []
                            inside_line = True
                        case '.value ', val:
                            if inside_line:
                                current_case.append(val.strip())
                        case '.case', *_:
                            if current_case:
                                output_lines.append(' '.join(current_case))
                                current_case = []
                            inside_line = False
                        case _:
                            continue

                if current_case:
                    output_lines.append(' '.join(current_case))

                return output_lines
        except FileNotFoundError as e:
            raise CfpRuntimeError from e
        
    def parse_lines_output(outputfile) -> list:
        try:
            with open(outputfile, 'r') as file:
                output_lines = []
                current_case = []
                num_cases = 0
                inside_line = False
                for line in file:
                    match line.strip().split('='):
                        # case '.numCases ', value:
                        #     num_cases = int(value.strip())
                        #     output_lines.append(str(num_cases))
                        case '.line', *_:
                            if current_case:
                                output_lines.append(' '.join(current_case))
                                current_case = []
                            inside_line = True
                        case '.value ', val:
                            if inside_line:
                                current_case.append(val.strip())
                        case '.case', *_:
                            if current_case:
                                output_lines.append(' '.join(current_case))
                                current_case = []
                            inside_line = False
                        case _:
                            continue

                if current_case:
                    output_lines.append(' '.join(current_case))

                return output_lines
        except FileNotFoundError as e:
            raise CfpRuntimeError from e
        
    @classmethod
    def input_file_fmt_1_to_input(cls, inputfile: str):
        output_lines = cls.parse_lines(inputfile)
        with open('temp.txt', 'w') as temp:
            for line in output_lines:
                temp.write(line + '\n')

        # result = ''.join(output_lines)
        # print(result.stdout, end='')

        with open('temp.txt', 'r') as temp:
            for line in temp:
                print(line.rstrip('\n'))

        os.remove('temp.txt')           
