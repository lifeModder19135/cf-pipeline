from enum import Enum
from .cfp_errors import CfpValueError

class ContestType(Enum):
    CF = 0
    IOI = 1
    ICPC =  2 

class Phase(Enum):
    BEFORE = 0
    CODING = 1
    PENDING_SYSTEM_TEST = 2
    SYSTEM_TEST = 3
    FINISHED = 4
    
class ContestCategory(Enum):
    """
    Values for property Contest.kind
    """
    OFFICIAL_ICPC_CONTEST = 0
    OFFICIAL_SCHOOL_CONTEST = 1
    OPENCUP_CONTEST = 2
    SCHOOL_CHAMPIONSHIP = 3
    UNIVERSITY_CHAMPIONSHIP = 4
    CITY_CHAMPIONSHIP = 5
    REGIONAL_CHAMPIONSHIP = 6
    TRAINING_CAMP_CONTEST = 7
    OFFICIAL_INTERNATIONAL_PERSONAL_CONTEST = 8
    TRAINING_CONTEST = 9

class Contest:
    """
    Represents a Contest object in an Api return value
    """
    
    @property
    def contest_id(self)->str:
        """Enum: CF, IOI, ICPC. Scoring system used for the contest."""
        return self.__contest_id
    
    @contest_id.setter
    def contest_id(self, cid: str)->None:
        self.__contest_id = cid

    @property
    def name(self)->str:
        """String containing contest name."""
        return self.__name

    @name.setter
    def name(self, name: str)->None:
        self.__name = name

    @property
    def contest_type(self)->str:
        """Enum: CF, IOI, ICPC. Scoring system used for the contest."""
        return self.__contest_type

    @contest_type.setter
    def contest_type(self, ct: str)->None:
        self.__contest_type = ct
        
    @property
    def phase(self) -> Phase:
        """ Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED."""
        return self.__phase

    @phase.setter
    def phase(self, phase:Phase) -> None:
        self.__phase = phase

    @property
    def frozen(self) -> bool:
        """If true, then the ranklist for the contest is frozen and shows only submissions, created before freeze."""
        return self.__is_frozen

    @frozen.setter
    def frozen(self, isfrozen:bool) -> None:
        self.__is_frozen = isfrozen

    @property
    def duration_seconds(self) -> str:
        """Duration of the contest in seconds."""
        return self.__duration_seconds

    @duration_seconds.setter
    def duration_seconds(self, dur: str) -> None:
        self.__duration_seconds = dur
        
    @property
    def start_time_seconds(self) -> int:
        """Can be absent. Contest start time in unix format."""
        return self.__start_time_seconds

    @start_time_seconds.setter
    def start_time_seconds(self, st_sec:int) -> None:
        self.__start_time_seconds = st_sec

    @property
    def relative_time_seconds(self) -> int:
        """Can be absent. Number of seconds, passed after the start of the contest. Can be negative."""
        return self.__relative_time_seconds

    @relative_time_seconds.setter
    def relative_time_seconds(self, rt_seconds:int) -> None:
        self.__relative_time_seconds = rt_seconds

    @property
    def prepared_by(self)->str:
        """Can be absent. Handle of the user, who created the contest."""
        return self.__prepared_by
    
    @prepared_by.setter
    def prepared_by(self, prep: str)->None:
        self.__prepared_by = prep

    @property
    def website_url(self) -> str:
        """Can be absent. URL for contest-related website."""
        return self.__website_url

    @website_url.setter
    def website_url(self, url: str) -> None:
        self.__website_url = url

    @property
    def description(self) -> str:
        """Localized. Can be absent."""
        return self.__description

    @description.setter
    def description(self, desc: str) -> None:
        self.__description = desc
        
    @property
    def difficulty(self) -> int:
        """Can be absent. From 1 to 5. Larger number means more difficult problems."""
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, diff:int) -> None:
        if diff >= 1 and diff <= 5:
            self.__difficulty = diff
        elif not diff: 
            if not self.__difficulty:
                self.__difficulty = -1
        else:
            raise CfpValueError

    @property
    def kind(self) -> bool:
        """Localized. Can be absent. Human-readable type of the contest from the following categories: Official ICPC Contest, Official School Contest, Opencup Contest, School/University/City/Region Championship, Training Camp Contest, Official International Personal Contest, Training Contest."""
        return self.__kind

    @kind.setter
    def kind(self, k:str) -> None:
        self.__kind = k

    @property
    def icpc_region(self) -> str:
        """# Localized. Can be absent. Name of the Region for official ICPC contests."""
        return self.__icpc_region

    @duration_seconds.setter
    def icpc_region(self, ir: str) -> None:
        self.__icpc_region = ir
        
    @property
    def country(self) -> int:
        """Localized. Can be absent."""
        return self.__country

    @country.setter
    def country(self, ctry:str) -> None:
        self.__country = ctry

    @property
    def city(self) -> int:
        """Localized. Can be absent."""
        return self.__city

    @city.setter
    def city(self, city:int) -> None:
        self.__city = city

    @property
    def season(self) -> str:
        """Can be absent."""
        return self.__season

    @season.setter
    def season(self, season:str) -> None:
        self.__season = season

#    contest_type: str = ''  
#    phase: str = ''  # Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.
#    frozen: bool =False # If true, then the ranklist for the contest is frozen and shows only submissions, created before freeze.
#    durationSeconds: int = -1 # Duration of the contest in seconds.
#    startTimeSeconds: int = -1 # Can be absent. Contest start time in unix format.
#    relativeTimeSeconds: int = -1 # Can be absent. Number of seconds, passed after the start of the contest. Can be negative.
#    preparedBy: str = ''  # Can be absent. Handle of the user, who created the contest.
#    websiteUrl: str = ''  # Can be absent. URL for contest-related website.
#    description: str = ''  # Localized. Can be absent.
#    difficulty: int = -1 # Can be absent. From 1 to 5. Larger number means more difficult problems.
#    kind: str = ''  # Localized. Can be absent. Human-readable type of the contest from the following categories: Official ICPC Contest, Official School Contest, Opencup Contest, School/University/City/Region Championship, Training Camp Contest, Official International Personal Contest, Training Contest.
#    icpcRegion: str = ''  # Localized. Can be absent. Name of the Region for official ICPC contests.
#    country: str = ''  # Localized. Can be absent.
#    city: str = ''  # Localized. Can be absent.
#    season: str = ''  # Can be absent.

    def __init__(self,contest_id: int, name: str,
                contest_type: str, phase: str,
                frozen: bool, durationSeconds: int,
                startTimeSeconds: int, relativeTimeSeconds: int,preparedBy: str, websiteUrl: str,
                description: str, difficulty: int,
                kind: str, icpcRegion: str,
                country: str, city: str, season: str
    ):
        self.contest_id(contest_id)
        self.name(name)
        self.contest_type(contest_type)
        self.phase(phase)
        self.frozen(frozen)
        self.duration_seconds(durationSeconds)
        self.start_time_seconds(startTimeSeconds)
        self.relative_time_seconds(relativeTimeSeconds)
        self.prepared_by(preparedBy)
        self.website_url(websiteUrl)
        self.description(description)
        self.difficulty(difficulty)
        self.kind(kind)
        self.icpc_region(icpcRegion)
        self.country(country)
        self.city(city)
        self.season(season)                         

# contest_id: int = -1
# name: str = ''  # Localized.
# contest_type: str = ''  # Enum: CF, IOI, ICPC. Scoring system used for the contest.
# phase: str = ''  # Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.
# frozen: bool # If true, then the ranklist for the contest is frozen and shows only submissions, created before freeze.
# durationSeconds: int = -1 # Duration of the contest in seconds.
# startTimeSeconds: int = -1 # Can be absent. Contest start time in unix format.
# relativeTimeSeconds: int = -1 # Can be absent. Number of seconds, passed after the start of the contest. Can be negative.
# preparedBy: str = ''  # Can be absent. Handle of the user, how created the contest.
# websiteUrl: str = ''  # Can be absent. URL for contest-related website.
# description: str = ''  # Localized. Can be absent.
# difficulty: int = -1 # Can be absent. From 1 to 5. Larger number means more difficult problems.
# kind: str = ''  # Localized. Can be absent. Human-readable type of the contest from the following categories: Official ICPC Contest, Official School Contest, Opencup Contest, School/University/City/Region Championship, Training Camp Contest, Official International Personal Contest, Training Contest.
# icpcRegion: str = ''  # Localized. Can be absent. Name of the Region for official ICPC contests.
# country: str = ''  # Localized. Can be absent.
# city: str = ''  # Localized. Can be absent.
# season: str = ''  # Can be absent.