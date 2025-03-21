from SOURCE.modules import cfp_contest


def test_create_contest_test():

    cntst = cfp_contest.Contest(
        'test id',
        'test name',
        'test type',
        'test phase',
        False,
        100,
        100,
        100,
        'tester',
        'https://www.test.com',
        'test description',
        3,
        'test kind',
        'test region',
        'test country',
        'test city',
        'test season'
    )
    assert cntst.city == 'test city'
    assert cntst.contest_id == 'test id'
    assert cntst.description == 'test description'