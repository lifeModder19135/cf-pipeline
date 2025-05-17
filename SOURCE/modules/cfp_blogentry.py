from json import loads

class BlogEntry:

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id) -> None:
        self.__id = id

    @property
    def originalLocale(self):
        return self.__origloc

    @originalLocale.setter
    def originalLocale(self, loc):
        self.__origloc = loc

    @property
    def creationTimeSeconds(self):
        return self.__ctis

    @creationTimeSeconds.setter
    def creationTimeSeconds(self, time):
        self.__ctis = time

    @property
    def authorHandle(self):
        return self.__authorhandle

    @authorHandle.setter
    def authorHandle(self, handle):
        self.__authorhandle = handle

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, t):
        self.__title = t

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, cont):
        self.__content = cont

    @property
    def locale(self):
        return self.__loc

    @locale.setter
    def locale(self, loc):
        self.__loc = loc

    @property
    def modificationTimeSeconds(self):
        return self.__mts

    @modificationTimeSeconds.setter
    def modificationTimeSeconds(self, time):
        self.__mts = time

    @property
    def allowViewHistory(self):
        return self.__avh

    @allowViewHistory.setter
    def allowViewHistory(self, avh):
        self.__avh = avh

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, t):
        self.__tags = t

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, r):
        self.__rating = r

    def __init__(self, id, origloc, cts, handle, title, content, loc, mts, avh, tags, rating):
        self.id = id
        self.originalLocale = origloc
        self.creationTimeSeconds = cts
        self.authorHandle = handle
        self.title = title
        self.content = content
        self.locale = loc
        self.modificationTimeSeconds = mts
        self.allowViewHistory = avh
        self.tags = tags
        self.rating = rating

    @classmethod
    def from_json(cls, jstr: str):
        jdct = loads(jstr)
        return cls(**jdct)
    
    @classmethod
    def list_from_json(cls, jstr: str):
        """Takes in a json list of blog entry objects and returns a python list of BlogEntry objects"""
        output_list = []
        py_list = loads(jstr)
        for blogentry in py_list:
            output_list.append(BlogEntry(**blogentry))
        return output_list

# id 	Integer.
# originalLocale 	String. Original locale of the blog entry.
# creationTimeSeconds 	Integer. Time, when blog entry was created, in unix format.
# authorHandle 	String. Author user handle.
# title 	String. Localized.
# content 	String. Localized. Not included in short version.
# locale 	String.
# modificationTimeSeconds 	Integer. Time, when blog entry has been updated, in unix format.
# allowViewHistory 	Boolean. If true, you can view any specific revision of the blog entry.
# tags 	String list.
# rating 	Integer.