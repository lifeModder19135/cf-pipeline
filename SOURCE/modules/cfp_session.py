from requests import Session
from SOURCE.modules.cfp_config import Configuration, ConfigSection
from bs4 import BeautifulSoup
from SOURCE.modules.cfp_errors import CfpIOError


class CfSession:

    __csrf_token: None = None
    
    @property
    def username(self):
        return self.__uname
    
    @username.setter
    def username(self, un: str):
        self.__uname = un

    @property
    def password(self):
        return self.__pwd

    @password.setter
    def password(self, pwd: str):
        self.__pwd = pwd

    @property
    def api_key(self):
        return self.__key
    
    @api_key.setter
    def api_key(self, key):
        self.__key = key

    @property
    def secret(self):
        return self.__secret
    
    @secret.setter
    def secret(self, secret: str):
        self.__secret = secret

    @property
    def config(self) -> Configuration:
        return self.__config
    
    @config.setter
    def config(self, conf: Configuration) -> None:
        self.__config = conf

    @property
    def csrf_token(self) -> str:
        return self.__csrf_token

    @csrf_token.setter
    def csrf_token(self, token: str) -> None:
        self.__csrf_token = token

    def __init__(self, username: str, pwd: str, key: str, secret: str, config: Configuration=None) -> None:
        self.session = Session()
        self.username = username
        self.password = pwd
        self.api_key = key
        self.secret = secret
        self.config = config
        self.set_csrf_token('https://codeforces.com/enter')
        self.logged_in = self.login()

    def login(self) -> bool:
        url = 'https://codeforces.com/enter'
        data = {'csrf_token': self.csrf_token,
            'action': 'enter',
            'handleOrEmail': self.username,
            'password': self.password}

        response = self.session.post(url=url, 
                                data=data, 
                                headers={'X-Csrf-Token': self.csrf_token}, 
                                allow_redirects=True)
        ok = response.ok
        ok = response.ok
        # text = BeautifulSoup(response.text, 'html.parser')
        # try:
        #     result = text.find_all("div", {"class": "lang-chooser"})[0].find_all('a')
        # except IndexError:
        #     raise CfpIOError('Login request failed. The server response was not what was expected.')
        # if result[-1].string.strip() == 'Register':
        #     return False
        
        return True
        
    def set_csrf_token(self, url):
        response = self.session.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')
        # try:
        #     token = bs.find_all('meta', {'name': 'csrf-token'})[0]['data-csrf']
        # except IndexError:
        #     raise CfpIOError('The html response did not contain a csrf token.')
        # self.csrf_token = token


if __name__ == '__main__':
    sec1 = ConfigSection('s1', 'a section', {})
    sec2 = ConfigSection('s2', 'a section', {})
    conf = Configuration('/test/path', 'test.conf', [sec1, sec2])
    sess = CfSession('lifeModder19135', 'Cadence_alexess1', '22baff2b22c33c42f3508343048de5ff00ce5dc8', 'd3abf51b55a859e138e5b37b3e00eca05ae9ac7d')
    
