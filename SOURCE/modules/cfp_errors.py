
class CfpInitializationError(RuntimeError):
    """
    Thrown when initialization of an object is attempted via the wrong method. Some objects can only be initialized via class methods. If direct invocation of the init method is attempted for any of these, this error must be thrown.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpUserInputError(IOError):
    """Catch-all for anything caused by invalid user input."""
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpMethodInputError(CfpUserInputError):
    """
    Thrown when initialization or method call of an object is attempted with the wrong parameters. 
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpTypeError(TypeError):
    """
    Just a custom fascade for TypeErrors
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpOverwriteNotAllowedError(CfpInitializationError):
    """
    Called when a setter tries to overwrite a property that has already been set and does not allow overwrites in the current context.
    Best Practice: when writing a setter for a collection/Iterable type property that holds multiple values, an overwriting call may be an attempt to update, append, etc. In this case include an extra kwarg of form 'overwrite:bool = False' and raise this error unless it is explicitly set to true. This way, the user still has the option to overwrite, but the afforementioned mishap is eliminated.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)