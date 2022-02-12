class McfpTestFixture(dictionary):
    
    def describe(self, output_fmt: string):
        """
        params:        
            <: output_fmt :: string :> 
                    must expand to any of the values in ['def', 'silent', 'short', 'mid', 'long']
                        ?'def'>> default; re-expands to one of the remaining 4, depending on config setting       OUTPUT_VERBOSITY_USER_DEF
                        ?'silent'>> silent-mode; no output returned
                        ?'short'>>  short-mode; very little output returned
                        ?'mid'>> mid-length mode; medium amt of output returned; default if OUTPUT_VERBOSITY_USER_DEF unset
                        ?'long'>> long-mode; verbose output returned
        """
    
    def setdescription(self,dscrptn: str):
        self[desc] = dscrptn
        
    def printdescription(self):
        if self[desc]:
            print(self[desc])
            return True
        else:
            raise IOError
        
    def __parse_wildcards_and_validate_str(content:any, strict:bool=False,contentFrom:str='list', ):
        """
        params:
            <: strict :: boolean :>
                    ''
            <: strict :: boolean :>  
                    False>> ('wildcards `*` and `?` enabled') :: True>> ('strict mode, no wildcards') 
            <: valuesFrom :: string :> 
                    'Values must be one of ( 'list' || 'dict' || 'envdict' || 'envlist' )'
        """
        pass