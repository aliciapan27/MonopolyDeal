from dataclasses import dataclass
from enums import PropertyColour
from card import *

# Data classes to structure the data clearly
@dataclass
class PropertyCardInfo:
    name: str
    colour: PropertyColour
    full_set: int

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

PROPERTY_CARD_DATA = [
    PropertyCardInfo("Mediterranean Avenue", PropertyColour.BROWN, 2),
    PropertyCardInfo("Baltic Avenue", PropertyColour.BROWN, 2),
    PropertyCardInfo("Oriental Avenue", PropertyColour.LIGHT_BLUE, 3),
    PropertyCardInfo("Vermont Avenue", PropertyColour.LIGHT_BLUE, 3),
    PropertyCardInfo("Connecticut Avenue", PropertyColour.LIGHT_BLUE, 3),
    PropertyCardInfo("St. Charles Place", PropertyColour.PINK, 3),
    PropertyCardInfo("States Avenue", PropertyColour.PINK, 3),
    PropertyCardInfo("Virginia Avenue", PropertyColour.PINK, 3),
    PropertyCardInfo("St. James Place", PropertyColour.ORANGE, 3),
    PropertyCardInfo("Tennessee Avenue", PropertyColour.ORANGE, 3),
    PropertyCardInfo("New York Avenue", PropertyColour.ORANGE, 3),
    PropertyCardInfo("Kentucky Avenue", PropertyColour.RED, 3),
    PropertyCardInfo("Indiana Avenue", PropertyColour.RED, 3),
    PropertyCardInfo("Illinois Avenue", PropertyColour.RED, 3),
    PropertyCardInfo("Atlantic Avenue", PropertyColour.YELLOW, 3),
    PropertyCardInfo("Ventnor Avenue", PropertyColour.YELLOW, 3),
    PropertyCardInfo("Marvin Gardens", PropertyColour.YELLOW, 3),
    PropertyCardInfo("Pacific Avenue", PropertyColour.GREEN, 3),
    PropertyCardInfo("North Carolina Avenue", PropertyColour.GREEN, 3),
    PropertyCardInfo("Pennsylvania Avenue", PropertyColour.GREEN, 3),
    PropertyCardInfo("Park Place", PropertyColour.DARK_BLUE, 2),
    PropertyCardInfo("Boardwalk", PropertyColour.DARK_BLUE, 2),
    PropertyCardInfo("Reading Railroad", PropertyColour.RAILROAD, 3),
    PropertyCardInfo("Pennsylvania Railroad", PropertyColour.RAILROAD, 3),
    PropertyCardInfo("B&O Railroad", PropertyColour.RAILROAD, 3),
    PropertyCardInfo("Short Line", PropertyColour.RAILROAD, 3),
    PropertyCardInfo("Electric Company", PropertyColour.UTILITY, 2),
    PropertyCardInfo("Water Works", PropertyColour.UTILITY, 2),
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
