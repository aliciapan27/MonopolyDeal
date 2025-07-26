from dataclasses import dataclass
from game_logic.enums import PropertyColour
from game_logic.card import *

@dataclass
class PropertyCardInfo:
    name: str
    colour: PropertyColour
    full_set: int
    value: int

@dataclass
class ActionCardInfo:
    cls: type
    count: int
    value: int

@dataclass
class RentCardInfo:
    colours: tuple[PropertyColour, ...]
    count: int
    value: int

@dataclass
class WildCardInfo:
    colours: tuple[PropertyColour, ...]
    count: int
    value: int

#{value: count}
MONEY_DATA = {1: 6, 2: 5, 3: 3, 4: 3, 5: 2, 10: 1}

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

PROPERTY_VALUES = {
    PropertyColour.BROWN: 1,
    PropertyColour.LIGHT_BLUE: 1,
    PropertyColour.PINK: 2,
    PropertyColour.ORANGE: 2,
    PropertyColour.RED: 3,
    PropertyColour.YELLOW: 3,
    PropertyColour.GREEN: 4,
    PropertyColour.DARK_BLUE: 4,
    PropertyColour.RAILROAD: 2,
    PropertyColour.UTILITY: 2
}

PROPERTY_RENT = {
    PropertyColour.BROWN: [1, 2],
    PropertyColour.LIGHT_BLUE: [1, 2, 3],
    PropertyColour.PINK: [1, 2, 4],
    PropertyColour.ORANGE: [1, 3, 5],
    PropertyColour.RED: [2, 3, 6],
    PropertyColour.YELLOW: [2, 4, 6],
    PropertyColour.GREEN: [2, 4, 7],
    PropertyColour.DARK_BLUE: [3, 8],
    PropertyColour.RAILROAD: [1, 2, 3, 4],
    PropertyColour.UTILITY: [1, 2]
}


PROPERTY_CARD_DATA = [
    PropertyCardInfo("Mediterranean Avenue", PropertyColour.BROWN, FULL_SET_SIZES[PropertyColour.BROWN], PROPERTY_VALUES[PropertyColour.BROWN]),
    PropertyCardInfo("Baltic Avenue", PropertyColour.BROWN, FULL_SET_SIZES[PropertyColour.BROWN], PROPERTY_VALUES[PropertyColour.BROWN]),
    PropertyCardInfo("Oriental Avenue", PropertyColour.LIGHT_BLUE, FULL_SET_SIZES[PropertyColour.LIGHT_BLUE], PROPERTY_VALUES[PropertyColour.LIGHT_BLUE]),
    PropertyCardInfo("Vermont Avenue", PropertyColour.LIGHT_BLUE, FULL_SET_SIZES[PropertyColour.LIGHT_BLUE], PROPERTY_VALUES[PropertyColour.LIGHT_BLUE]),
    PropertyCardInfo("Connecticut Avenue", PropertyColour.LIGHT_BLUE, FULL_SET_SIZES[PropertyColour.LIGHT_BLUE], PROPERTY_VALUES[PropertyColour.LIGHT_BLUE]),
    PropertyCardInfo("St. Charles Place", PropertyColour.PINK, FULL_SET_SIZES[PropertyColour.PINK], PROPERTY_VALUES[PropertyColour.PINK]),
    PropertyCardInfo("States Avenue", PropertyColour.PINK, FULL_SET_SIZES[PropertyColour.PINK], PROPERTY_VALUES[PropertyColour.PINK]),
    PropertyCardInfo("Virginia Avenue", PropertyColour.PINK, FULL_SET_SIZES[PropertyColour.PINK], PROPERTY_VALUES[PropertyColour.PINK]),
    PropertyCardInfo("St. James Place", PropertyColour.ORANGE, FULL_SET_SIZES[PropertyColour.ORANGE], PROPERTY_VALUES[PropertyColour.ORANGE]),
    PropertyCardInfo("Tennessee Avenue", PropertyColour.ORANGE, FULL_SET_SIZES[PropertyColour.ORANGE], PROPERTY_VALUES[PropertyColour.ORANGE]),
    PropertyCardInfo("New York Avenue", PropertyColour.ORANGE, FULL_SET_SIZES[PropertyColour.ORANGE], PROPERTY_VALUES[PropertyColour.ORANGE]),
    PropertyCardInfo("Kentucky Avenue", PropertyColour.RED, FULL_SET_SIZES[PropertyColour.RED], PROPERTY_VALUES[PropertyColour.RED]),
    PropertyCardInfo("Indiana Avenue", PropertyColour.RED, FULL_SET_SIZES[PropertyColour.RED], PROPERTY_VALUES[PropertyColour.RED]),
    PropertyCardInfo("Illinois Avenue", PropertyColour.RED, FULL_SET_SIZES[PropertyColour.RED], PROPERTY_VALUES[PropertyColour.RED]),
    PropertyCardInfo("Atlantic Avenue", PropertyColour.YELLOW, FULL_SET_SIZES[PropertyColour.YELLOW], PROPERTY_VALUES[PropertyColour.YELLOW]),
    PropertyCardInfo("Ventnor Avenue", PropertyColour.YELLOW, FULL_SET_SIZES[PropertyColour.YELLOW], PROPERTY_VALUES[PropertyColour.YELLOW]),
    PropertyCardInfo("Marvin Gardens", PropertyColour.YELLOW, FULL_SET_SIZES[PropertyColour.YELLOW], PROPERTY_VALUES[PropertyColour.YELLOW]),
    PropertyCardInfo("Pacific Avenue", PropertyColour.GREEN, FULL_SET_SIZES[PropertyColour.GREEN], PROPERTY_VALUES[PropertyColour.GREEN]),
    PropertyCardInfo("North Carolina Avenue", PropertyColour.GREEN, FULL_SET_SIZES[PropertyColour.GREEN], PROPERTY_VALUES[PropertyColour.GREEN]),
    PropertyCardInfo("Pennsylvania Avenue", PropertyColour.GREEN, FULL_SET_SIZES[PropertyColour.GREEN], PROPERTY_VALUES[PropertyColour.GREEN]),
    PropertyCardInfo("Park Place", PropertyColour.DARK_BLUE, FULL_SET_SIZES[PropertyColour.DARK_BLUE], PROPERTY_VALUES[PropertyColour.DARK_BLUE]),
    PropertyCardInfo("Boardwalk", PropertyColour.DARK_BLUE, FULL_SET_SIZES[PropertyColour.DARK_BLUE], PROPERTY_VALUES[PropertyColour.DARK_BLUE]),
    PropertyCardInfo("Reading Railroad", PropertyColour.RAILROAD, FULL_SET_SIZES[PropertyColour.RAILROAD], PROPERTY_VALUES[PropertyColour.RAILROAD]),
    PropertyCardInfo("Pennsylvania Railroad", PropertyColour.RAILROAD, FULL_SET_SIZES[PropertyColour.RAILROAD], PROPERTY_VALUES[PropertyColour.RAILROAD]),
    PropertyCardInfo("B&O Railroad", PropertyColour.RAILROAD, FULL_SET_SIZES[PropertyColour.RAILROAD], PROPERTY_VALUES[PropertyColour.RAILROAD]),
    PropertyCardInfo("Short Line", PropertyColour.RAILROAD, FULL_SET_SIZES[PropertyColour.RAILROAD], PROPERTY_VALUES[PropertyColour.RAILROAD]),
    PropertyCardInfo("Electric Company", PropertyColour.UTILITY, FULL_SET_SIZES[PropertyColour.UTILITY], PROPERTY_VALUES[PropertyColour.UTILITY]),
    PropertyCardInfo("Water Works", PropertyColour.UTILITY, FULL_SET_SIZES[PropertyColour.UTILITY], PROPERTY_VALUES[PropertyColour.UTILITY]),
]

ACTION_DATA = [
    ActionCardInfo(DealBreakerCard, 2, 5),
    ActionCardInfo(ForceDealCard, 3, 3),
    ActionCardInfo(SlyDealCard, 3, 3),
    ActionCardInfo(JustSayNoCard, 3, 4),
    ActionCardInfo(DebtCollectorCard, 3, 3),
    ActionCardInfo(BirthdayCard, 3, 2),
    ActionCardInfo(DoubleRentCard, 2, 1),
    ActionCardInfo(HouseCard, 3, 3),
    ActionCardInfo(HotelCard, 2, 4),
    ActionCardInfo(PassGoCard, 10, 1),
]

RENT_CARDS_DATA = [
    RentCardInfo((PropertyColour.DARK_BLUE, PropertyColour.GREEN), 2, 1),
    RentCardInfo((PropertyColour.PINK, PropertyColour.ORANGE), 2, 1),
    RentCardInfo((PropertyColour.RED, PropertyColour.YELLOW), 2, 1),
    RentCardInfo((PropertyColour.LIGHT_BLUE, PropertyColour.BROWN), 2, 1),
    RentCardInfo((PropertyColour.RAILROAD, PropertyColour.UTILITY), 2, 1),
    RentCardInfo((PropertyColour.ANY,), 3, 3),
]

WILDCARD_DATA = [
    WildCardInfo((PropertyColour.DARK_BLUE, PropertyColour.GREEN), 1, 4),
    WildCardInfo((PropertyColour.LIGHT_BLUE, PropertyColour.BROWN), 1, 1),
    WildCardInfo((PropertyColour.GREEN, PropertyColour.RAILROAD), 1, 4),
    WildCardInfo((PropertyColour.LIGHT_BLUE, PropertyColour.RAILROAD), 1, 4),
    WildCardInfo((PropertyColour.RAILROAD, PropertyColour.UTILITY), 1, 2),
    WildCardInfo((PropertyColour.PINK, PropertyColour.ORANGE), 2, 2),
    WildCardInfo((PropertyColour.RED, PropertyColour.YELLOW), 2, 3),
    WildCardInfo((PropertyColour.ANY,), 2, 0),
]

