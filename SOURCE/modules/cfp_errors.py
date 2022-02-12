
class CfpInitializationError(RuntimeError):
    """
    Thrown when initialization of an object is attempted via the wrong method. Some objects can only be initialized via class methods. If direct invocation of the init method is attempted for any of these, this error must be thrown.
    """
    pass

class CfpUserInputError(IOError):
    """Catchall for anything caused by invalid user input."""
    pass

class CfpMethodInputError(CfpUserInputError):
    """
    Thrown when initialization or method call of an object is attempted with the wrong parameters. 
    """
    pass

