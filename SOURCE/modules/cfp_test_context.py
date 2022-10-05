import os, subprocess
from .cfp_errors import CfpRuntimeError, CfpValueError
from .cfp_context import CfpFile, CfpRunner, LanguageChoice, LanguageType

class SimpleInputHandler:
    pass

class SimpleSourceHandler():
    pass

class SimpleCodeforcesTester(CfpRunner):
    """
    Description: simple_tester 
    Methods: [set_callstr(), 

        
        


    """
    LANG_TYPE = LanguageType.OTHER

    def set_callstr(self, lang:LanguageChoice):
        try:
            match lang:
                case LanguageChoice.C_SHARP_MONO:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.D_DMD32:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.DELPHI:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.FREE_PASCAL:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.GO:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.HASKELL:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.JAVA_11:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.JAVA_8:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.JS_V8:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.KOTLIN_14:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.KOTLIN_15:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.NODE_JS:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.OCAML:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.PERL:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.PASCAL_ABC_DOT_NET:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.PHP:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.PYTHON_2:
                    self.LANG_TYPE = LanguageType.INTERPRETED

                    return str()
                case LanguageChoice.PYTHON_3:
                    self.LANG_TYPE = LanguageType.INTERPRETED
                case LanguageChoice.PYPY_2:
                    self.LANG_TYPE = LanguageType.INTERPRETED
                case LanguageChoice.PYPY_3:
                    self.LANG_TYPE = LanguageType.INTERPRETED
                case LanguageChoice.RUBY:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.RUST:
                    self.LANG_TYPE = LanguageType.OTHER
                case LanguageChoice.SCALA:
                    self.LANG_TYPE = LanguageType.OTHER
        except BaseException as e:
            raise CfpRuntimeError from e

    def __setup_pipes(self, lang:LanguageChoice, input_string:str, source_file:CfpFile):
        """
        Description: simple_tester. Should take in a tuple of the format (lang, formatted_input_string, source_file)     
        Params:
            lang (LanguageChoice): 
                
                The language in which the source file is written. Used to determine the compiler / interpreter to invoke.
        """
        self.set_(lang)
        if self.LANG_TYPE == LanguageType.OTHER:
            raise CfpValueError
        elif self.LANG_TYPE == LanguageType.INTERPRETED:


            output_str = str(input_string) + ' | ' + str(src_call)

    def simple_source_handler(self, lang:LanguageChoice, input_string:str, source_file:CfpFile):
        """
        Description: simple_tester. Should take in a tuple of the format (lang, formatted_input_string, source_file)     
        Params:
            lang (LanguageChoice): 
                The language in which the source file is written. Used to determine the compiler / interpreter to invoke.
            input
        """

    def run(lang,input_file:CfpFile,source_file:CfpFile):
        # ps1 = subprocess.run(input=subprocess.STDIN, output=subprocess.PIPE)
        pass