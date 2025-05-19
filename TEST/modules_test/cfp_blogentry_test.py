from SOURCE.modules.cfp_blogentry import BlogEntry
import json

def test_create_blogentry_test():
    be = BlogEntry('test loc', False, 100, 100, 'testhandle', 100, 100, 'Test Title', 'test loc', ['test1', 'test2'])
    assert be.id == 100
    assert be.originalLocale == 'test loc'
    assert be.creationTimeSeconds == 100
    assert be.authorHandle == 'testhandle'
    assert be.title == 'Test Title'
    assert be.locale == 'test loc'
    assert be.modificationTimeSeconds == 100
    assert be.allowViewHistory == False
    assert be.tags[0] == 'test1'
    assert be.tags[1] == 'test2'
    assert be.rating == 100

def test_blogentry_from_json_test():
    json = '''
        {
            "originalLocale":"ru",
            "allowViewHistory":false,
            "creationTimeSeconds":1415106466,
            "rating":782,
            "authorHandle":"Fefer_Ivan",
            "modificationTimeSeconds":1415119106,
            "id":14580,
            "title":"\u003cp\u003eAndrew Stankevich Contests — 46 contests later\u003c/p\u003e",
            "locale":"en",
            "tags":[
                "asc",
                "codeforces"
            ]
        }
    '''
    be = BlogEntry.from_json(json)
    assert be.allowViewHistory == False

def test_blogentry_list_from_json_test():
    with open('/home/ntolb/CODING_PROJECTS/python_workspaces/0-vscode_ws/cf-pipeline/RESOURCES/test_resources/user.blogEntries?handle=Fefer_Ivan', 'r') as file:
        json_obj = json.load(file)
        json_str = json.dumps(json_obj)
        be = BlogEntry.list_from_json(json_str)
