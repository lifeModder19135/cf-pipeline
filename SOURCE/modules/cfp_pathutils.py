from urllib.parse import urlparse, urlunparse
import webbrowser

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
    def __init__(self, url):
        self.url_full = url
        url_p = urlparse(url)
        self.parseresult = url_p
        self.scheme = url_p.scheme
        self.fragment = url_p.fragment
        self.location = url_p.netloc
        self.query = url_p.query
        self.params = url_p.params
        self.path = url_p.path

    def open(self):
        webbrowser.open(self.url_full)

    def todict(self):
        dct = {'scheme': self.scheme, 'base_url': self.location, 'path': self.path, 'query': self.query, 'params': self.params, 'fragment': self.fragment}
        return dct
    
    def construct(self):
        components = (self.scheme, self.location, self.path, self.params, self.query, self.fragment)
        return urlunparse(components)
