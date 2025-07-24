from enum import Enum, auto

class CardType(Enum):
    MONEY = auto()
    PROPERTY = auto()
    ACTION = auto()

class PropertyColour(Enum):
    BROWN = auto()
    LIGHT_BLUE = auto()
    PINK = auto()
    ORANGE = auto()
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    DARK_BLUE = auto()
    RAILROAD = auto() #Black
    UTILITY = auto() #Mint
    ANY = auto()

class ActionType(Enum):
    HOUSE = auto()
    HOTEL = auto()
    PASS_GO = auto()
    BIRTHDAY = auto()
    DEBT_COLLECTOR = auto()
    FORCE_DEAL = auto()
    SLY_DEAL = auto()
    JUST_SAY_NO = auto()
    DEAL_BREAKER = auto()
    DOUBLE_RENT = auto()
    RENT = auto()