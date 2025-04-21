from SOURCE.modules.cfp_problem import Problem, ProblemType
import pytest
from SOURCE.modules.cfp_errors import CfpTypeError

def test_create_problem_test():
    tags = ['test', 'test tag', 'test tag 2']
    pr = Problem(contestId=1, problemset_name='test problemset', index='a', name='test problem', type=ProblemType.CF_PROGRAMMING, points=float(100), rating=100, tags=tags)

    assert pr.contest_id == 1
    assert pr.index == 'a'
    assert pr.problemset_name == 'test problemset'
    assert pr.name == 'test problem'
    assert pr.type == ProblemType.CF_PROGRAMMING
    assert pr.points == float(100)
    assert pr.rating == 100
    assert pr.tags == ['test', 'test tag', 'test tag 2']

def test_problem_failsproperly_test():
    tags = ['test', 'test tag', 'test tag 2']
    with pytest.raises(CfpTypeError):
        pr = Problem(1, 'test problemset', 'a', 'test problem', 'test type', float(100), 100, tags)
