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

FULL_SET_SIZES = {
    PropertyColour.BROWN: 2,
    PropertyColour.LIGHT_BLUE: 3,
    PropertyColour.PINK: 3,
    PropertyColour.ORANGE: 3,
    PropertyColour.RED: 3,
    PropertyColour.YELLOW: 3,
    PropertyColour.GREEN: 3,
    PropertyColour.DARK_BLUE: 2,
    PropertyColour.RAILROAD: 4,
    PropertyColour.UTILITY: 2
}

