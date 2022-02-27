class Contest:
    contest_id: int = -1
    name: string = ''  # Localized.
    contest_type: string = ''  # Enum: CF, IOI, ICPC. Scoring system used for the contest.
    phase: string = ''  # Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.
    frozen: bool # If true, then the ranklist for the contest is frozen and shows only submissions, created before freeze.
    durationSeconds: int = -1 # Duration of the contest in seconds.
    startTimeSeconds: int = -1 # Can be absent. Contest start time in unix format.
    relativeTimeSeconds: int = -1 # Can be absent. Number of seconds, passed after the start of the contest. Can be negative.
    preparedBy: string = ''  # Can be absent. Handle of the user, how created the contest.
    websiteUrl: string = ''  # Can be absent. URL for contest-related website.
    description: string = ''  # Localized. Can be absent.
    difficulty: int = -1 # Can be absent. From 1 to 5. Larger number means more difficult problems.
    kind: string = ''  # Localized. Can be absent. Human-readable type of the contest from the following categories: Official ICPC Contest, Official School Contest, Opencup Contest, School/University/City/Region Championship, Training Camp Contest, Official International Personal Contest, Training Contest.
    icpcRegion: string = ''  # Localized. Can be absent. Name of the Region for official ICPC contests.
    country: string = ''  # Localized. Can be absent.
    city: string = ''  # Localized. Can be absent.
    season: string = ''  # Can be absent.


    def __init__(self,contest_id: int, name: string,
                contest_type: string, phase: string,
                frozen: bool, durationSeconds: int,
                startTimeSeconds: int, relativeTimeSeconds: int,preparedBy: string, websiteUrl: string,
                description: string, difficulty: int,
                kind: string, icpcRegion: string,
                country: string, city: string, season: string
    ):
        self.contest_id = contest_id
        self.name = name
        self.contest_type = contest_type
        self.phase = phase
        self.frozen = frozen
        self.durationSeconds = durationSeconds
        self.startTimeSeconds =startTimeSeconds
        self.relativeTimeSeconds = relativeTimeSeconds
        self.preparedBy = preparedBy
        self.websiteUrl = websiteUrl
        self.description = description
        self.difficulty = difficulty
        self.kind = kind
        self.icpcRegion = icpcRegion
        self.country = country
        self.city = city
        self.season =  season                         
        
        














