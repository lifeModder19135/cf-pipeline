class McfpTestFixture(dictionary):
    
    def describe(self, outputFmt: string):
        """
        params:        
            <: valuesFrom :: string :> 
                    must expand to any of the values in ['def', 'silent', 'short', 'mid', 'long']
                        ?'def'>> 

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