from .libcfapi_constants import CFP_CONTEXT_DIRECTORY_BASE as ctx_base, CFP_CONTEXT_DIRECTORY_NAME as ctx_dirname
from ..libcfp_errors import CfpSetupError, CfpCtxDirectoryMissingError




#################### PATH UTILS ###########################################       

def resolve_context_location_base():
    if ctx_base is None or ctx_dirname is None:
        raise CfpSetupError('either the inner module libcfapi_constants is missing, or else required constants are undefined')
    elif 
        if
    return ''.join(ctx_base, ctx_dirname)
