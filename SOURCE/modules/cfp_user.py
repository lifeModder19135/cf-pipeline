from pathlib import Path


class User:
    
    def get_blogposts():
        pass
    
    def set_blogposts():
        pass
   
    @property 
    def handle(self)-> str:
        return self.__handle

    @handle.setter
    def handle(self, val:str)-> None:
        self.__handle = val

    @property
    def email(self)-> str:
        return self.__email

    @email.setter
    def email(self, email:str)-> None:
        self.__email = email

    @property 
    def vkid(self)-> str:
        return self.__vkid

    @vkid.setter
    def vkid(self, id:str)-> None:
        self.__vkid = id

    @property
    def openid(self)-> str:
        return self.__openid

    @openid.setter
    def openid(self, id:str)-> None:
        self.__openid = id
    
    @property 
    def firstname(self)-> str:
        return self.__f_name

    @firstname.setter
    def firstname(self, fname:str)-> None:
        self.__f_name = fname

    @property
    def lastname(self)-> str:
        return self.__l_name

    @lastname.setter
    def lastname(self, lname:str)-> None:
        self.__l_name = lname

    @property 
    def country(self)-> str:
        return self.__country

    @country.setter
    def country(self, cntry)-> None:
        self.__country = cntry

    @property
    def city(self)-> str:
        return self.__city

    @city.setter
    def city(self, city)-> str:
        self.__city = city
    
    @property
    def organization(self)-> str:
        return self.__organization

    @organization.setter
    def organization(self, org:str)-> None:
        self.__organization = org

    @property
    def contribution(self)-> int:
        return self.__contribution

    @contribution.setter
    def contribution(self, cont:int)-> None:
        self.__contribution = cont

    @property
    def rank(self)-> str:
        return self.__rank

    @rank.setter
    def rank(self,rnk:str)-> None:
        self.__rank = rnk

    @property
    def rating(self)-> int:
        return self.__rating

    @rating.setter
    def rating(self, rtng:int)-> None:
        self.__rating = rtng

    @property
    def max_rank(self)-> str:
        return self.__max_rank

    @max_rank.setter
    def max_rank(self,rnk:str)-> None:
        self.__max_rank = rnk

    @property
    def max_rating(self)-> int:
        return self.__max_rating

    @max_rating.setter
    def max_rating(self, rtng:int)-> None:
        self.__max_rating = rtng

    @property
    def last_online_time_seconds(self)-> int:
        return self.__last_online

    @last_online_time_seconds.setter
    def last_online_time_seconds(self, time:int)-> None:
        self.__last_online = time

    @property
    def registration_time_seconds(self)-> int:
        return self.__reg_time

    @registration_time_seconds.setter
    def registration_time_seconds(self, time:int)-> None:
        self.__reg_time = time

    @property 
    def friend_of_count(self)-> int:
        return self.__friend_of_count

    @friend_of_count.setter
    def friend_of_count(self, foc:int)-> None:
        self.__friend_of_count = foc

    @property
    def avatar(self)-> str:
        return self.__avatar

    @avatar.setter
    def avatar(self, avatar:str)-> None:
        self.__avatar = avatar

    @property 
    def title_photo(self)-> Path:
        return self.__title_photo

    @title_photo.setter
    def title_photo(self, path:Path)-> None:
        self.__title_photo = path

#    handle = '' # Codeforces user handle
#    email: str = '' # Shown only if user allowed to share his contact info
#    vkId: str = '' # User id for VK social network. Shown only if user allowed to share his contact info.
#    openId: str = '' # Shown only if user allowed to share his contact info.
#    firstName: str = '' # Localized. Can be absent.
#    lastName: str = '' # Localized. Can be absent.
#    country: str = '' # Localized. Can be absent.
#    city: str = '' # Localized. Can be absent.
#    organization: str = '' # Localized. Can be absent.
#    contribution: int = 0 # User contribution.
#    rank: str = '' # Localized.
#    rating: int = -1 
#    maxRank: str = '' # Localized.
#    maxRating: int = -1 
#    lastOnlineTimeSeconds: int = -1 # Time, when user was last seen online, in unix format.
#    registrationTimeSeconds: int = -1 # Time, when user was registered, in unix format.
#    friendOfCount: int = -1 # Amount of users who have this user in friends.
#    avatar: str = '' # User's avatar URL.
#    titlePhoto: str = '' # User's title photo URL.    
    
    
    def __init__(self, handle: str, email: str, vkId: str, openId: str, firstName: str, lastName: str, country: str, city: str, organization: str, contribution: int,rank: str, rating: int, maxRank: str, maxRating: int, lastOnlineTimeSeconds: int, registrationTimeSeconds: int, friendOfCount: int, avatar: str, titlePhoto: str):
        self.handle(handle)
        self.email(email)
        self.vkid(vkId)
        self.openid(openId)
        self.firstname(firstName)
        self.lastname(lastName)
        self.country(country)
        self.city(city)
        self.organization(organization)
        self.contribution(contribution)
        self.rank(rank)
        self.rating(rating)
        self.max_rank(maxRank)
        self.max_rating(maxRating)
        self.last_online_time_seconds(lastOnlineTimeSeconds)
        self.registration_time_seconds(registrationTimeSeconds)
        self.friend_of_count(friendOfCount)
        self.avatar(avatar)
        self.title_photo(titlePhoto)
    