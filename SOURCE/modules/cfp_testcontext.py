import os, subprocess
from SOURCE.modules.cfp_context import CfpFile
from SOURCE.modules.cfp_errors import CfpRuntimeError
from pathlib import Path
import subprocess
from subprocess import run

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

    @classmethod
    def input_file_fmt_1_to_input(cls, inputfile: str):
        with open('temp.txt', 'w') as temp:
            try:
                with open(inputfile, 'r') as file:
                    case = 0
                    line = 0
                    case1line1 = ''
                    case1line2 = ''
                    case1line3 = ''
                    case1line4 = ''
                    case1line5 = ''
                    case1line6 = ''
                    case1line7 = ''
                    case1line8 = ''
                    case1line9 = ''
                    case1line10 = ''
                    case2line1 = ''
                    case2line2 = ''
                    case2line3 = ''
                    case2line4 = ''
                    case2line5 = ''
                    case2line6 = ''
                    case2line7 = ''
                    case2line8 = ''
                    case2line9 = ''
                    case2line10 = ''
                    case3line1 = ''
                    case3line2 = ''
                    case3line3 = ''
                    case3line4 = ''
                    case3line5 = ''
                    case3line6 = ''
                    case3line7 = ''
                    case3line8 = ''
                    case3line9 = ''
                    case3line10 = ''
                    case4line1 = ''
                    case4line2 = ''
                    case4line3 = ''
                    case4line4 = ''
                    case4line5 = ''
                    case4line6 = ''
                    case4line7 = ''
                    case4line8 = ''
                    case4line9 = ''
                    case4line10 = ''
                    case5line1 = ''
                    case5line2 = ''
                    case5line3 = ''
                    case5line4 = ''
                    case5line5 = ''
                    case5line6 = ''
                    case5line7 = ''
                    case5line8 = ''
                    case5line9 = ''
                    case5line10 = ''
                    case6line1 = ''
                    case6line2 = ''
                    case6line3 = ''
                    case6line4 = ''
                    case6line5 = ''
                    case6line6 = ''
                    case6line7 = ''
                    case6line8 = ''
                    case6line9 = ''
                    case6line10 = ''
                    case7line1 = ''
                    case7line2 = ''
                    case7line3 = ''
                    case7line4 = ''
                    case7line5 = ''
                    case7line6 = ''
                    case7line7 = ''
                    case7line8 = ''
                    case7line9 = ''
                    case7line10 = ''
                    case8line1 = ''
                    case8line2 = ''
                    case8line3 = ''
                    case8line4 = ''
                    case8line5 = ''
                    case8line6 = ''
                    case8line7 = ''
                    case8line8 = ''
                    case8line9 = ''
                    case8line10 = ''
                    case9line1 = ''
                    case9line2 = ''
                    case9line3 = ''
                    case9line4 = ''
                    case9line5 = ''
                    case9line6 = ''
                    case9line7 = ''
                    case9line8 = ''
                    case9line9 = ''
                    case9line10 = ''
                    case10line1 = ''
                    case10line2 = ''
                    case10line3 = ''
                    case10line4 = ''
                    case10line5 = ''
                    case10line6 = ''
                    case10line7 = ''
                    case10line8 = ''
                    case10line9 = ''
                    case10line10 = ''
                    for lne in file.readlines():
                        cleanline = lne.lstrip().rstrip()
                        if cleanline.startswith('.numCases'):
                            split = cleanline.split(' ')
                            value = str(split[2]) + '\n'
                            temp.write(value)
                            
                        elif cleanline.startswith('.case'):
                            case += 1
                        elif cleanline.startswith('.line'):
                            line += 1
                        elif cleanline.startswith('.value') and case == 1 and line == 1:
                            print(str(cleanline.split(' ')[2]))
                            case1line1 = case1line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 1:
                            case2line1 = case2line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 1:
                            case3line1 = case3line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 1:
                            case4line1 = case4line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 1:
                            case5line1 = case5line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 1:
                            case6line1 = case6line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 1:
                            case7line1 = case7line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 1:
                            case8line1 = case8line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 1:
                            case9line1 = case9line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 1:
                            case10line1 = case10line1 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 2:
                            case1line2 = case1line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 2:
                            case2line2 = case2line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 2:
                            case3line2 = case3line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 2:
                            case4line2 = case4line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 2:
                            case5line2 = case5line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 2:
                            case6line2 = case6line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 2:
                            case7line2 = case7line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 2:
                            case8line2 = case8line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 2:
                            case9line2 = case9line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 2:
                            case10line2 = case10line2 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 3:
                            case1line3 = case1line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 3:
                            case2line3 = case2line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 3:
                            case3line3 = case3line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 3:
                            case4line3 = case4line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 3:
                            case5line3 = case5line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 3:
                            case6line3 = case6line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 3:
                            case7line3 = case7line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 3:
                            case8line3 = case8line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 3:
                            case9line3 = case9line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 3:
                            case10line3 = case10line3 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 4:
                            case1line4 = case1line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 4:
                            case2line4 = case2line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 4:
                            case3line4 = case3line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 4:
                            case4line4 = case4line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 4:
                            case5line4 = case5line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 4:
                            case6line4 = case6line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 4:
                            case7line4 = case7line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 4:
                            case8line4 = case8line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 4:
                            case9line4 = case9line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 4:
                            case10line4 = case10line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 5:
                            case1line4 = case1line4 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 5:
                            case2line5 = case2line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 5:
                            case3line5 = case3line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 5:
                            case4line5 = case4line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 5:
                            case5line5 = case5line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 5:
                            case6line5 = case6line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 5:
                            case7line5 = case7line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 5:
                            case8line5 = case8line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 5:
                            case9line5 = case9line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 5:
                            case10line5 = case10line5 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 6:
                            case1line6 = case1line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 6:
                            case2line6 = case2line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 6:
                            case3line6 = case3line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 6:
                            case4line6 = case4line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 6:
                            case5line6 = case5line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 6:
                            case6line6 = case6line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 6:
                            case7line6 = case7line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 6:
                            case8line6 = case8line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 6:
                            case9line6 = case9line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 6:
                            case10line6 = case10line6 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 7:
                            case1line7 = case1line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 7:
                            case2line7 = case2line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 7:
                            case3line7 = case3line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 7:
                            case4line7 = case4line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 7:
                            case5line7 = case5line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 7:
                            case6line7 = case6line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 7:
                            case7line7 = case7line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 7:
                            case8line7 = case8line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 7:
                            case9line7 = case9line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 7:
                            case10line7 = case10line7 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 8:
                            case1line8 = case1line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 8:
                            case2line8 = case2line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 8:
                            case3line8 = case3line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 8:
                            case4line8 = case4line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 8:
                            case5line8 = case5line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 8:
                            case6line8 = case6line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 8:
                            case7line8 = case7line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 8:
                            case8line8 = case8line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 8:
                            case9line8 = case9line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 8:
                            case10line8 = case10line8 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 9:
                            case1line9 = case1line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 9:
                            case2line9 = case2line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 9:
                            case3line9 = case3line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 9:
                            case4line9 = case4line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 9:
                            case5line9 = case5line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 9:
                            case6line9 = case6line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 9:
                            case7line9 = case7line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 9:
                            case8line9 = case8line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 9:
                            case9line9 = case9line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 9:
                            case10line9 = case10line9 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 1 and line == 10:
                            case1line10 = case1line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 2 and line == 10:
                            case2line10 = case2line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 3 and line == 10:
                            case3line10 = case3line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 4 and line == 10:
                            case4line10 = case4line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 5 and line == 10:
                            case5line10 = case5line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 6 and line == 10:
                            case6line10 = case6line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 7 and line == 10:
                            case7line10 = case7line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 8 and line == 10:
                            case8line10 = case8line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 9 and line == 10:
                            case9line10 = case9line10 + str(cleanline.split(' ')[2]) + ' '
                        elif cleanline.startswith('.value') and case == 10 and line == 10:
                            case10line10 = case10line10 + str(cleanline.split(' ')[2]) + ' '
                        else:
                            pass
                        
                        if case1line1 != '':
                            temp.write(case1line1)
                            temp.write('\n')
                        elif case1line2 != '':
                            temp.write(case1line2)
                            temp.write('\n')
                        elif case1line3 != '':
                            temp.write(case1line3)
                            temp.write('\n')
                        elif case1line4 != '':
                            temp.write(case1line4)
                            temp.write('\n')
                        elif case1line5 != '':
                            temp.write(case1line5)
                            temp.write('\n')
                        elif case1line6 != '':
                            temp.write(case1line6)
                            temp.write('\n')
                        elif case1line7 != '':
                            temp.write(case1line7)
                            temp.write('\n')
                        elif case1line8 != '':
                            temp.write(case1line8)
                            temp.write('\n')
                        elif case1line9 != '':
                            temp.write(case1line9)
                            temp.write('\n')
                        elif case1line10 != '':
                            temp.write(case1line10)
                            temp.write('\n')

                        elif case2line1 != '':
                            temp.write(case2line1)
                            temp.write('\n')
                        elif case2line2 != '':
                            temp.write(case2line2)
                            temp.write('\n')
                        elif case2line3 != '':
                            temp.write(case2line3)
                            temp.write('\n')
                        elif case2line4 != '':
                            temp.write(case2line4)
                            temp.write('\n')
                        elif case2line5 != '':
                            temp.write(case2line5)
                            temp.write('\n')
                        elif case2line6 != '':
                            temp.write(case2line6)
                            temp.write('\n')
                        elif case2line7 != '':
                            temp.write(case2line7)
                            temp.write('\n')
                        elif case2line8 != '':
                            temp.write(case2line8)
                            temp.write('\n')
                        elif case2line9 != '':
                            temp.write(case2line9)
                            temp.write('\n')
                        elif case2line10 != '':
                            temp.write(case2line10)
                            temp.write('\n')

                        elif case3line1 != '':
                            temp.write(case3line1)
                            temp.write('\n')
                        elif case3line2 != '':
                            temp.write(case3line2)
                            temp.write('\n')
                        elif case3line3 != '':
                            temp.write(case3line3)
                            temp.write('\n')
                        elif case3line4 != '':
                            temp.write(case3line4)
                            temp.write('\n')
                        elif case3line5 != '':
                            temp.write(case3line5)
                            temp.write('\n')
                        elif case3line6 != '':
                            temp.write(case3line6)
                            temp.write('\n')
                        elif case3line7 != '':
                            temp.write(case3line7)
                            temp.write('\n')
                        elif case3line8 != '':
                            temp.write(case3line8)
                            temp.write('\n')
                        elif case3line9 != '':
                            temp.write(case3line9)
                            temp.write('\n')
                        elif case3line10 != '':
                            temp.write(case3line10)
                            temp.write('\n')

                        elif case4line1 != '':
                            temp.write(case4line1)
                            temp.write('\n')
                        elif case4line2 != '':
                            temp.write(case4line2)
                            temp.write('\n')
                        elif case4line3 != '':
                            temp.write(case4line3)
                            temp.write('\n')
                        elif case4line4 != '':
                            temp.write(case4line4)
                            temp.write('\n')
                        elif case4line5 != '':
                            temp.write(case4line5)
                            temp.write('\n')
                        elif case4line6 != '':
                            temp.write(case4line6)
                            temp.write('\n')
                        elif case4line7 != '':
                            temp.write(case4line7)
                            temp.write('\n')
                        elif case4line8 != '':
                            temp.write(case4line8)
                            temp.write('\n')
                        elif case4line9 != '':
                            temp.write(case4line9)
                            temp.write('\n')
                        elif case4line10 != '':
                            temp.write(case4line10)
                            temp.write('\n')

                        elif case5line1 != '':
                            temp.write(case5line1)
                            temp.write('\n')
                        elif case5line2 != '':
                            temp.write(case5line2)
                            temp.write('\n')
                        elif case5line3 != '':
                            temp.write(case5line3)
                            temp.write('\n')
                        elif case5line4 != '':
                            temp.write(case5line4)
                            temp.write('\n')
                        elif case5line5 != '':
                            temp.write(case5line5)
                            temp.write('\n')
                        elif case5line6 != '':
                            temp.write(case5line6)
                            temp.write('\n')
                        elif case5line7 != '':
                            temp.write(case5line7)
                            temp.write('\n')
                        elif case5line8 != '':
                            temp.write(case5line8)
                            temp.write('\n')
                        elif case5line9 != '':
                            temp.write(case5line9)
                            temp.write('\n')
                        elif case5line10 != '':
                            temp.write(case5line10)
                            temp.write('\n')

                        elif case6line1 != '':
                            temp.write(case6line1)
                            temp.write('\n')
                        elif case6line2 != '':
                            temp.write(case6line2)
                            temp.write('\n')
                        elif case6line3 != '':
                            temp.write(case6line3)
                            temp.write('\n')
                        elif case6line4 != '':
                            temp.write(case6line4)
                            temp.write('\n')
                        elif case6line5 != '':
                            temp.write(case6line5)
                            temp.write('\n')
                        elif case6line6 != '':
                            temp.write(case6line6)
                            temp.write('\n')
                        elif case6line7 != '':
                            temp.write(case6line7)
                            temp.write('\n')
                        elif case6line8 != '':
                            temp.write(case6line8)
                            temp.write('\n')
                        elif case6line9 != '':
                            temp.write(case6line9)
                            temp.write('\n')
                        elif case6line10 != '':
                            temp.write(case6line10)
                            temp.write('\n')

                        elif case7line1 != '':
                            temp.write(case7line1)
                            temp.write('\n')
                        elif case7line2 != '':
                            temp.write(case7line2)
                            temp.write('\n')
                        elif case7line3 != '':
                            temp.write(case7line3)
                            temp.write('\n')
                        elif case7line4 != '':
                            temp.write(case7line4)
                            temp.write('\n')
                        elif case7line5 != '':
                            temp.write(case7line5)
                            temp.write('\n')
                        elif case7line6 != '':
                            temp.write(case7line6)
                            temp.write('\n')
                        elif case7line7 != '':
                            temp.write(case7line7)
                            temp.write('\n')
                        elif case7line8 != '':
                            temp.write(case7line8)
                            temp.write('\n')
                        elif case7line9 != '':
                            temp.write(case7line9)
                            temp.write('\n')
                        elif case7line10 != '':
                            temp.write(case7line10)
                            temp.write('\n')

                        elif case8line1 != '':
                            temp.write(case8line1)
                            temp.write('\n')
                        elif case2line8 != '':
                            temp.write(case8line2)
                            temp.write('\n')
                        elif case8line3 != '':
                            temp.write(case8line3)
                            temp.write('\n')
                        elif case8line4 != '':
                            temp.write(case8line4)
                            temp.write('\n')
                        elif case8line5 != '':
                            temp.write(case8line5)
                            temp.write('\n')
                        elif case8line6 != '':
                            temp.write(case8line6)
                            temp.write('\n')
                        elif case8line7 != '':
                            temp.write(case8line7)
                            temp.write('\n')
                        elif case8line8 != '':
                            temp.write(case8line8)
                            temp.write('\n')
                        elif case8line9 != '':
                            temp.write(case8line9)
                            temp.write('\n')
                        elif case8line10 != '':
                            temp.write(case8line10)
                            temp.write('\n')

                        elif case9line1 != '':
                            temp.write(case9line1)
                            temp.write('\n')
                        elif case9line2 != '':
                            temp.write(case9line2)
                            temp.write('\n')
                        elif case9line3 != '':
                            temp.write(case9line3)
                            temp.write('\n')
                        elif case9line4 != '':
                            temp.write(case9line4)
                            temp.write('\n')
                        elif case9line5 != '':
                            temp.write(case9line5)
                            temp.write('\n')
                        elif case9line6 != '':
                            temp.write(case9line6)
                            temp.write('\n')
                        elif case9line7 != '':
                            temp.write(case9line7)
                            temp.write('\n')
                        elif case9line8 != '':
                            temp.write(case9line8)
                            temp.write('\n')
                        elif case9line9 != '':
                            temp.write(case9line9)
                            temp.write('\n')
                        elif case9line10 != '':
                            temp.write(case9line10)
                            temp.write('\n')

                        elif case10line1 != '':
                            temp.write(case10line1)
                            temp.write('\n')
                        elif case10line2 != '':
                            temp.write(case10line2)
                            temp.write('\n')
                        elif case10line3 != '':
                            temp.write(case10line3)
                            temp.write('\n')
                        elif case10line4 != '':
                            temp.write(case10line4)
                            temp.write('\n')
                        elif case10line5 != '':
                            temp.write(case10line5)
                            temp.write('\n')
                        elif case10line6 != '':
                            temp.write(case10line6)
                            temp.write('\n')
                        elif case10line7 != '':
                            temp.write(case10line7)
                            temp.write('\n')
                        elif case10line8 != '':
                            temp.write(case10line8)
                            temp.write('\n')
                        elif case10line9 != '':
                            temp.write(case10line9)
                            temp.write('\n')
                        elif case10line10 != '':
                            temp.write(case10line10)
                            temp.write('\n')

                        result = run('cat temp.txt', shell=True, capture_output=True)
                        print(result.stdout)
                                
            except FileNotFoundError as e:
                raise CfpRuntimeError from e
