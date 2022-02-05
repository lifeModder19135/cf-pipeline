class CfpInitializationError(RuntimeError):
    """
    Thrown when initialization of an object is attempted via the wrong method. Some objects can only be initialized via class methods. If direct invocation of the init method is attempted for any of these, this error must be thrown.
    """
    pass

class CfpMethodInputError(IOException):
    """
    Thrown when initialization or method call of an object is attempted with the wrong parameters. 
    """
    pass

