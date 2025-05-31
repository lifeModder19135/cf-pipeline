from SOURCE.modules.cfp_user import User
from SOURCE.modules.cfp_errors import CfpTypeError
from pytest import raises
from pathlib import Path

def test_user_failsproperly_test():

    with raises(CfpTypeError):
        user = User(lastName='Smith',
                    country='USA', 
                    lastOnlineTimeSeconds=999, 
                    city='New York', 
                    rating=888, 
                    friendOfCount=123,
                    titlePhoto='/test/path',
                    handle='test_handle',
                    avatar='test/path/to/avatar',
                    firstName='Larry',
                    contribution=777,
                    organization='TestOrg',
                    rank='master',                  
                    maxRating=888,
                    registrationTimeSeconds=1010101,
                    maxRank='master',
                    email='test@email.com', 
                    vkId='testid', 
                    openId='test_openid', 
                   )
        user.title_photo = 'not a path'

def test_create_user_test():
    user = User(lastName='Smith',
                country='USA', 
                lastOnlineTimeSeconds=999, 
                city='New York', 
                rating=888, 
                friendOfCount=123,
                titlePhoto='/test/path',
                handle='test_handle',
                avatar='test/path/to/avatar',
                firstName='Larry',
                contribution=777,
                organization='TestOrg',
                rank='master',                  
                maxRating=888,
                registrationTimeSeconds=1010101,
                maxRank='master',
                email='test@email.com', 
                vkId='testid', 
                openId='test_openid', 
                )
    assert user.handle == 'test_handle'
    assert user.email == 'test@email.com'
    assert user.vkid == 'testid'
    assert user.openid == 'test_openid'
    assert user.firstname == 'Larry'
    assert user.lastname == 'Smith'
    assert user.country == 'USA'
    assert user.city == 'New York'
    assert user.organization == 'TestOrg'
    assert user.contribution == 777

def test_user_from_json_test():
    stub = '{"lastName":"Fefer","country":"Russia","lastOnlineTimeSeconds":1672070012,"city":"Saratov","rating":2174,"friendOfCount":415,"titlePhoto":"https://userpic.codeforces.org/242/title/151ab49dee0779f8.jpg","handle":"Fefer_Ivan","avatar":"https://userpic.codeforces.org/242/avatar/c4e6a102a9e66281.jpg","firstName":"Ivan","contribution":0,"organization":"Booking.com","rank":"master","maxRating":2476,"registrationTimeSeconds":1264960450,"maxRank":"grandmaster"}'
    user = User.from_json(stub)
    assert user.lastname == 'Fefer'
    assert user.country == 'Russia'

def test_user_from_json_response_0objects_test():
    stub = '{"status":"OK","result":[]}'
    users = User.from_json_response(stub)
    assert users == None

def test_user_from_json_response_1object_test():
    stub = '{"status":"OK","result":[{"lastName":"Fefer","country":"Russia","lastOnlineTimeSeconds":1672070012,"city":"Saratov","rating":2174,"friendOfCount":415,"titlePhoto":"https://userpic.codeforces.org/242/title/151ab49dee0779f8.jpg","handle":"Fefer_Ivan","avatar":"https://userpic.codeforces.org/242/avatar/c4e6a102a9e66281.jpg","firstName":"Ivan","contribution":0,"organization":"Booking.com","rank":"master","maxRating":2476,"registrationTimeSeconds":1264960450,"maxRank":"grandmaster"}]}'
    user = User.from_json_response(stub)
    assert type(user) == User
    assert user.firstname == 'Ivan'

def test_user_from_json_response_multiple_objects_test():
    stub = '{"status":"OK","result":[{"lastName":"Khodyrev","lastOnlineTimeSeconds":1742481459,"rating":1709,"friendOfCount":95,"titlePhoto":"https://userpic.codeforces.org/1592/title/27e43714e4bea090.jpg","handle":"DmitriyH","avatar":"https://userpic.codeforces.org/1592/avatar/7cef566902732053.jpg","firstName":"Dmitriy","contribution":0,"organization":"","rank":"expert","maxRating":2072,"registrationTimeSeconds":1268570311,"maxRank":"candidate master"},{"lastName":"Fefer","country":"Russia","lastOnlineTimeSeconds":1672070012,"city":"Saratov","rating":2174,"friendOfCount":415,"titlePhoto":"https://userpic.codeforces.org/242/title/151ab49dee0779f8.jpg","handle":"Fefer_Ivan","avatar":"https://userpic.codeforces.org/242/avatar/c4e6a102a9e66281.jpg","firstName":"Ivan","contribution":0,"organization":"Booking.com","rank":"master","maxRating":2476,"registrationTimeSeconds":1264960450,"maxRank":"grandmaster"}]}'
    users = User.from_json_response(stub)
    assert type(users) == list
    assert users[0].firstname == 'Dmitriy'
    assert users[1].firstname == 'Ivan'

def test_user_get_user_by_handle_test():
    user = User.get_user_by_handle('DmitriyH', check_historic_handles=True)
    assert user.handle == 'DmitriyH'
    assert user.firstname == 'Dmitriy'
    assert user.lastname == 'Khodyrev'

def test_user_get_user_by_handle_xtra_arg_omitted_test():
    user = User.get_user_by_handle('Dmitriy')
    assert user.handle == 'Dmitriy'
    assert user.registration_time_seconds == 1284545124

def test_user_get_blogposts_no_keyword_test():
    user = User.get_user_by_handle('Fefer_Ivan')
    blogposts = user.get_blogposts()
    assert blogposts[0].authorHandle == 'Fefer_Ivan'

def test_user_get_blogposts_with_keyword_test():
    user = User.get_user_by_handle('Fefer_Ivan')
    blogposts = user.get_blogposts(keyword='Stankevich')
    assert blogposts[0].authorHandle == 'Fefer_Ivan'
    assert blogposts[0].title == '<p>Andrew Stankevich Contests — 46 contests later</p>'

