from SOURCE.modules.cfp_blogentry import BlogEntry

def test_create_blogentry_test():
    be = BlogEntry(100, 'test loc', 100, 'testhandle', 'Test Title', 'This is a test.', 'test loc', 100, False, ['test1', 'test2'], 100)
    assert be.id == 100
    assert be.originalLocale == 'test loc'
    assert be.creationTimeSeconds == 100
    assert be.authorHandle == 'testhandle'
    assert be.title == 'Test Title'
    assert be.content == 'This is a test.'
    assert be.locale == 'test loc'
    assert be.modificationTimeSeconds == 100
    assert be.allowViewHistory == False
    assert be.tags[0] == 'test1'
    assert be.tags[1] == 'test2'
    assert be.rating == 100

    def test_blogentry_from_json_test():
        pass

    def test_blogentry_list_from_json_test():
        pass