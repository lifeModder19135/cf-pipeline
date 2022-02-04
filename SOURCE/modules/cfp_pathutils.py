from urllib import parse

class PathTool:
    '''
    Just a group of functions that will hellp in manipulating path strings, and in some cases, Path and other <path-like> objects.
    '''
def slashpath_remove_outermost_prefix(pathstr: str):
    '''
    Removes the outer directory. returns the smallest prefix path, the path equivalent to the input if cwd were the  
    '''
    lstripped: bool = False
    if pathstr.startswith("/"):   
        return ''.join('/',list(map(str, pathstr[1:].partition('/'))))
    else:
        return list(map(str, pathstr.partition('/')))

def slashpath_separate_filename_from_pathprefix(pathstr: str):
    pathstr.rstrip('/')
    return list(map(str, pathstr.rpartition('/')))

class cfp_url():
    '''
    Wrapper object for the named tuple returned by urllib parse function, which  takes in a url string and splits it into six sections: the protocol, net/host, params, path, attributes, and values 
    '''
    
    def __init__():
        parse.    