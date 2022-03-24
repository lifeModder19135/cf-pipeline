from urllib import parse

class PathTool:
    """
    Just a group of functions that will help in manipulating path strings, and in some cases, Path and other <path-like> objects.
    """
def slashpath_remove_outermost_prefix(path_str: str):
    """
    Removes the outer directory. returns the smallest prefix path, the path equivalent to the input if cwd were the  
    """
    lstripped: bool = False
    if path_str.startswith("/"):
        return ''.join('/', list(map(str, path_str[1:].partition('/'))))
    else:
        return list(map(str, path_str.partition('/')))

def slashpath_separate_filename_from_pathprefix(path_str: str):
    path_str.rstrip('/')
    return list(map(str, path_str.rpartition('/')))

class cfp_url():
    """
    Wrapper object for the named tuple returned by urllib parse function, which  takes in a url string and splits it into six sections: the protocol, net/host, params, path, attributes, and values
    """
    
    def __init__():
        parse.    