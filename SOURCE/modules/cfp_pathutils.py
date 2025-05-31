from urllib.parse import urlparse, urlunparse
import webbrowser
import os
import re

class PathTool:
    """
    This is a group of functions that will help in manipulating path strings, and in some cases, Path and other <path-like> objects. Right now, it only works on posix paths.
    """

    @staticmethod
    def slashpath_remove_outermost_prefix(path_str: str):
        """
        This removes the outer directory of an input path. It returns the smallest prefix path, the path equivalent to the input if cwd were the next directory in
        """
        if os.name == 'posix':
            sep = '/'
        else:
            sep = '\\'

        if path_str.startswith("/"):
            path_str = path_str[1:]
        elif bool(re.match('^[A-Z]:\\\\', path_str)):
            path_str = path_str[3:]

        path_lst = path_str.split(sep)
        new_path_lst = path_lst[1:]
        return sep.join(new_path_lst)

    @staticmethod
    def slashpath_separate_filename_from_pathprefix(path_str: str):
        """This takes a path and returns the directory structure, the separator, and the filename, in that order, in a list. Alternately, if the given path points to a directory, it will break off that last directory and return path-to-directory, separator, and directory in a list in that order."""
        isdir = False
        isabs = False
        if os.name == 'posix':
            sep = '/'
        else:
            sep = '\\'

        if path_str.endswith(sep):
            isdir = True

        if isdir == False:
            return list(map(str, path_str.rpartition(sep)))
        else:
            new_path = path_str.rstrip(sep)
            lst = new_path.split(sep)
            path_dir = lst[-1]
            prefix = sep.join(lst[:-1])

            result = [prefix, sep, path_dir]
            return result

        

class CfpUrl():
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
    
if __name__ == '__main__':
    res = PathTool.slashpath_separate_filename_from_pathprefix('C:\\home\\user\\download1.exe')
