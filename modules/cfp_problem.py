class Problem:
    contestId: int = -1       # Can be absent. Id of the contest, containing the problem.
    problemsetName: string = ''    # Can be absent. Short name of the problemset the problem belongs to.
    index: string = ''        # Usually, a letter or letter with digit(s) indicating the problem index in a contest.
    name: string = ''         # Localized.
    problem_type: string = '' # PROGRAMMING, QUESTION.
    points: float = float(-1) # Can be absent. Maximum amount of points for the problem.
    rating: int = -1          # Can be absent. Problem rating (difficulty).
    tags: list[string] = list()       # Problem tags.
    solved_by_user: bool = False
    
    def __init__(contestId: int, problemsetName: string, index: string, name: string, problemType: string, points: float, rating: int, tags: list[string]):
        self.contestId = contestId 
        self.problemset_name = problemsetName
        self.index = index 
        self.name = name
        if problem_type == '' or problem_type == '':
            self.problem_type = problem_type
        else:
            raise ValueError('Value of problem_type is invalid.')
        self.points = float(points)
        self.rating = rating
        self.tags = tags
        return True
    
    def mark_solved(self):
        self.solved_by_user = True
        return True
        
    def mark_unsolved(self):
        self.solved_by_user = False
        return True
        