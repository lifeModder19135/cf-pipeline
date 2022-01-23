class User:
    
    def get_blogposts():
        pass
    
    def set_blogposts():
        pass
   
     
    handle: string = '' # Codeforces user handle
    
    email: string = '' # Shown only if user allowed to share his contact info
    vkId: string = '' # User id for VK social network. Shown only if user allowed to share his contact info.
    openId: string = '' # Shown only if user allowed to share his contact info.
    firstName: string = '' # Localized. Can be absent.
    lastName: string = '' # Localized. Can be absent.
    country: string = '' # Localized. Can be absent.
    city: string = '' # Localized. Can be absent.
    organization: string = '' # Localized. Can be absent.
    contribution: int = 0 # User contribution.
    rank: string = '' # Localized.
    rating: int = -1 
    maxRank: string = '' # Localized.
    maxRating: int = -1 
    lastOnlineTimeSeconds: int = -1 # Time, when user was last seen online, in unix format.
    registrationTimeSeconds: int = -1 # Time, when user was registered, in unix format.
    friendOfCount: int = -1 # Amount of users who have this user in friends.
    avatar: string = '' # User's avatar URL.
    titlePhoto: string = '' # User's title photo URL.    
    
    
    def __init__(self, handle: string, email: string, vkId: string, openId: string, firstName: string, lastName: string, country: string, city: string, organization: string, contribution: int,rank: string, rating: int, maxRank: string, maxRating: int, lastOnlineTimeSeconds: int, registrationTimeSeconds: int, friendOfCount: int, avatar: string, titlePhoto: string):
        self.handle = handle
        self.email = email
        self.vkId = vkId
        self.openId = openId
        self.firstName = firstName
        self.lastName = lastName
        self.country = country
        self.city = city
        self.organization = organization
        self.contribution = contribution
        self.rank = rank
        self.rating = rating
        self.maxRank = maxRank
        self.maxRating = maxRating
        self.lastOnlineTimeSeconds = lastOnlineTimeSeconds
        self.registrationTimeSeconds = registrationTimeSeconds
        self.friendOfCount = friendOfCount
        self.avatar = avatar
        self.titlePhoto = titlePhoto
    
    def get_blogposts():
        pass
    
    def set_blogposts():
        pass