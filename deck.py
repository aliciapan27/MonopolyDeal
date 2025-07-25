from card import *
from enums import CardType
from card_data import *
import random

def create_money_cards():
    money_cards = []

    for value, count in MONEY_DATA.items():
        for _ in range(count):
            money_cards.append(MoneyCard(value))
    
    return money_cards

def create_property_cards():
    property_cards = []

    for prop_info in PROPERTY_CARD_DATA:
        property_cards.append(PropertyCard(prop_info.colour, prop_info.name, prop_info.full_set, prop_info.value))

    for wild_info in WILDCARD_DATA:
        property_cards.extend([WildCard(wild_info.colours, wild_info.value) for _ in range(wild_info.count)])

    return property_cards

def create_action_cards():
    action_cards = []

    for action_info in ACTION_DATA:
        action_cards.extend([action_info.cls(action_info.value) for _ in range(action_info.count)])

    for rent_info in RENT_CARDS_DATA:
        action_cards.extend([RentCard(rent_info.colours, rent_info.value) for _ in range(rent_info.count)])

    return action_cards
    
def create_deck():
    deck = []
    deck.extend(create_money_cards())
    deck.extend(create_action_cards())
    deck.extend(create_property_cards())

    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def create_test_deck():
    return [
        MoneyCard(1),
        MoneyCard(5),
        PropertyCard(PropertyColour.DARK_BLUE, "Park Place", 2),
        PropertyCard(PropertyColour.DARK_BLUE, "Boardwalk", 2),
        PropertyCard(PropertyColour.BROWN, "Baltic Avenue", 2),
        WildCard([PropertyColour.GREEN, PropertyColour.DARK_BLUE], 4),
        WildCard([PropertyColour.ANY], 0),

        HouseCard(3),
        HotelCard(4),
        DealBreakerCard(5),
        JustSayNoCard(3),
        SlyDealCard(3),
        JustSayNoCard(4),
        DebtCollectorCard(3),
        BirthdayCard(2),
        DoubleRentCard(1),
        PassGoCard(1),

        RentCard([PropertyColour.GREEN, PropertyColour.DARK_BLUE], 1),
        RentCard([PropertyColour.ANY], 3)
    ]

def create_test_hand1():
    return [
        PropertyCard(PropertyColour.DARK_BLUE, "Boardwalk", FULL_SET_SIZES[PropertyColour.DARK_BLUE], PROPERTY_VALUES[PropertyColour.DARK_BLUE]),
        WildCard([PropertyColour.GREEN, PropertyColour.DARK_BLUE], 4),
        RentCard([PropertyColour.ANY], 2),
        DoubleRentCard(1),
        HouseCard(3),
        BirthdayCard(2),
        JustSayNoCard(4),
        MoneyCard(1),
        MoneyCard(2)
    ]

def create_test_hand2():
    return [
        JustSayNoCard(4),
        DebtCollectorCard(3),
        BirthdayCard(2),
        DoubleRentCard(1),
        PassGoCard(1),
        MoneyCard(1),
        MoneyCard(2),
        MoneyCard(2)
    ]


#DEBUGGING
def print_deck_info(deck):
    counts = {
        CardType.MONEY: 0,
        CardType.PROPERTY: 0,
        CardType.ACTION: 0
    }

    for card in deck:
        counts[card.card_type] += 1

    total = len(deck)

    print(f"Deck info (total cards: {total}):")
    print(f"  Money cards:    {counts[CardType.MONEY]}")
    print(f"  Property cards: {counts[CardType.PROPERTY]}")
    print(f"  Action cards:   {counts[CardType.ACTION]}")

def print_full_deck(deck):
     # Debug print: list all cards in deck
    for card in deck:
        print(card)

