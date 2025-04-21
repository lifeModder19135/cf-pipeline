from enum import Enum
import json

from SOURCE.modules.cfp_errors import CfpTypeError
from .cfp_errors import CfpValueError

class ProblemType(Enum):
    CF_PROGRAMMING = 0
    CF_QUESTION = 1

class Problem(object):

    @property
    def contest_id(self) -> int:
        return self.__ctst_id
    
    @contest_id.setter
    def contest_id(self, id: int) -> None:
        self.__ctst_id = id        
    
    @property
    def problemset_name(self) -> str:
        return self.__problemset_name

    @problemset_name.setter
    def problemset_name(self, ps_name: str) -> None:
        self.__problemset_name = ps_name 

    @property
    def index(self) -> int:
        return self.__ndx

    @index.setter
    def index(self, index: int) -> None:
        self.__ndx = index

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @property
    def type(self) -> ProblemType:
        return self.__problem_type

    @type.setter
    def type(self, prob_type: ProblemType) -> None:
        # if prob_type == 'PROGRAMMING':
        self.__problem_type = prob_type

    @property
    def points(self) -> float:
        return self.__points

    @points.setter
    def points(self, points: float) -> None:
        self.__points = points

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, rating: int) -> None:
        self.__rating = rating

    @property
    def tags(self) -> list:
        if not self.__tags:
            self.__tags = []
        return self.__tags

    @tags.setter
    def tags(self, tag_list: list) -> None:
        if type(tag_list) is list:
            self.__tags = tag_list
        elif type(tag_list) is str:
            self.__tags = [tag_list]
        else:
            raise CfpTypeError

    @property
    def solved_by_user(self) -> bool:
        return self.__solved

    @index.setter
    def solved_by_user(self, sbu: bool) -> None:
        self.__solved = sbu

#    contestId: "int" = -1       # Can be absent. Id of the contest, containing the problem.
#    problemsetName: "string" = ''    # Can be absent. Short name of the problemset the problem belongs to.
#    index: "string" = ''        # Usually, a letter or letter with digit(s) indicating the problem index in a contest.
#    name: "string" = ''         # Localized.
#    problem_type: "string" = '' # PROGRAMMING, QUESTION.
#    points: "float" = float(-1) # Can be absent. Maximum amount of points for the problem.
#    rating: "int" = -1          # Can be absent. Problem rating (difficulty).
#    tags: "list[str]" = list()       # Problem tags.
#    solved_by_user: "bool" = False
    def __init__(self, contestId: int, index: str, name: str, type: str, points: float = '0', tags: list = None, problemset_name: str = None, rating: int = None):
        self.contest_id = contestId
        self.problemset_name = problemset_name
        self.index = index
        self.name = name
        self.type = type
        # if type(problem_type) is ProblemType:
        #     self.type = problem_type
        # else:
        #     raise CfpTypeError('Type of problem_type is invalid. You must pass a value of type ProblemType for this parameter.')
        self.points = points
        self.rating = rating
        self.tags = tags
        if self.type == 'PROGRAMMING':
            self.type = ProblemType.CF_PROGRAMMING
        elif self.type == 'QUESTION':
            self.type = ProblemType.CF_QUESTION
        elif self.type == ProblemType.CF_PROGRAMMING or self.type == ProblemType.CF_QUESTION:
            pass
        else: 
            raise CfpValueError('\"type\" attribute was passed an invalid value.')

    def __repr__(self):
        return f'\nProblem:\n\n  NAME: {self.name}\n  CONTEST: {self.contest_id}\n  INDEX: {self.index}\n  TYPE: {self.type}\n  POINTS: {self.points}\n  TAGS: {self.tags}\n'

    @classmethod
    def from_json(cls, j_str: str):
        """This takes in a string of json data and returns Problem objects representing that data."""
        j_dct = json.loads(str(j_str))
        return cls(**j_dct)
    
    @classmethod
    def from_dict(cls, jdct):
        """This takes in a dictionary of data and returns Problem objects filled with that data."""
        return cls(**jdct)
    
    def mark_solved(self, user):
        
        self.user = user
        self.solved_by_user = True
        return True
        
    def mark_unsolved(self, user):
        self.user = user
        self.solved_by_user = False
        return True
        