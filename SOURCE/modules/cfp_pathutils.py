from urllib import parse

class PathTool:
    """
    This is a group of functions that will help in manipulating path strings, and in some cases, Path and other <path-like> objects. Right now, it only works on posix paths.
    """
def slashpath_remove_outermost_prefix(path_str: str):
    """
    This removes the outer directory of an input path. It returns the smallest prefix path, the path equivalent to the input if cwd were the next directory in
    """
    lstripped: bool = False
    if path_str.startswith("/"):
        return ''.join('/', list(map(str, path_str[1:].partition('/'))))
    else:
        return list(map(str, path_str.partition('/')))

def slashpath_separate_filename_from_pathprefix(path_str: str):
    """This takes a path and returns both the directory structure and the filename, in that order, in a list."""
    path_str.rstrip('/')
    return list(map(str, path_str.rpartition('/')))

class cfp_url():
    """
    Not yet implemented. This will be a wrapper object for the named tuple returned by urllib parse function, which  takes in a url string and splits it into six sections: the protocol, net/host, params, path, attributes, and values
    TODO: write this class
    """
    pass
    # def __init__():
       