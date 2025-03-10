
class CfpInitializationError(RuntimeError):
    """
    Thrown when initialization of an object is attempted via the wrong method. Some objects can only be initialized via class methods. If direct invocation of the init method is attempted for any of these, this error must be thrown.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpIOError(IOError):
    """
    Wrapper class for IOError
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpConfigurationError(CfpIOError):
    """
    Catch-all for any configuration errors.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpUserInputError(CfpIOError):
    """
    Catch-all for anything caused by invalid user input.
    """
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

class CfpValueError(ValueError):
    """
    Just a custom fascade for ValueErrors
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        
class CfpPermissionDeniedError(PermissionError):
    """
    Fascade for PermissionErrors. If a bit of code will occasionally raise PermissionErrors, wrap it in a try loop and rais this in a subsequent 'except PermissionError:' loop
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpRuntimeError(RuntimeError):
    """
    Fascade for RuntimeErrors.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpOverwriteNotAllowedError(CfpRuntimeError):
    """
    Called when a process doesn't return within the predetermined time limit.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpNotExecutableError(CfpValueError):
    """
    Called when a method expects an executable program but gets something else.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

class CfpTimeoutError(CfpRuntimeError):
    """
    Called when a method expects an executable program but gets something else.
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)