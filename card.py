from enums import CardType, PropertyColour, FULL_SET_SIZES
from property_set import PropertySet


class Card:
    def __init__(self, name: str, card_type: CardType, value: int = 0):
        self.name = name
        self.card_type = card_type 
        self.value = value

    def __str__(self):
        return f"{self.name} ({self.card_type}, ${self.value}M)"


# Money and property cards
class MoneyCard(Card):
    def __init__(self, value):
        super().__init__(f"${value}M", CardType.MONEY, value)

class PropertyCard(Card):
    def __init__(self, colour, name, full_set):
        super().__init__(name, CardType.PROPERTY)
        self.colour = colour
        self.full_set = full_set
        # no monetary value
    def __str__(self):
        return f"{self.name}, {self.colour}, Full set:{ self.full_set} ({self.card_type}, ${self.value}M)"
              
class WildCard(Card):
    def __init__(self, colours, value):
        name = f"{'/'.join(colour.name.replace('_', ' ').title() for colour in colours)} Wildcard"
        super().__init__(name, CardType.PROPERTY, value)
        self.colours = colours

# Action cards
class HouseCard(Card):
    def __init__(self, value):
        super().__init__("House", CardType.ACTION, value)

class HotelCard(Card):
    def __init__(self, value):
        super().__init__("Hotel", CardType.ACTION, value)
        
class PassGoCard(Card):
    def __init__(self, value):
        super().__init__("PassGo", CardType.ACTION, value)
    
class BirthdayCard(Card):
    def __init__(self, value):
        super().__init__("It's My Birthday", CardType.ACTION, value)

class DebtCollectorCard(Card):
    def __init__(self, value):
        super().__init__("Debt Collector", CardType.ACTION, value)

class ForceDealCard(Card):
    def __init__(self, value):
        super().__init__("Force Deal", CardType.ACTION, value)

    def play(self, game, player, target_player):
        full_sets = [s for s in target_player.property_sets if s.is_full()]
        if not full_sets:
            print("No full sets to steal.")
            return
        # maybe just steal the first full set for now
        stolen_set = full_sets[0]
        target_player.property_sets.remove(stolen_set)
        player.property_sets.append(stolen_set)
        print(f"{player.name} used Deal Breaker and stole a full set from {target_player.name}")


class SlyDealCard(Card):
    def __init__(self, value):
        super().__init__("Sly Deal", CardType.ACTION, value)


class JustSayNoCard(Card):
    def __init__(self, value):
        super().__init__("Just Say No", CardType.ACTION, value)


class DealBreakerCard(Card):
    def __init__(self, value):
        super().__init__("Deal Breaker", CardType.ACTION, value)


class DoubleRentCard(Card):
    def __init__(self, value):
        super().__init__("Double Rent", CardType.ACTION, value)


# RENT CARDS

class RentCard(Card):
    def __init__(self, colours, value):
        name = f"{'/'.join(colour.name.replace('_', ' ').title() for colour in colours)} Rent"
        super().__init__(name, CardType.ACTION, value)
        self.colours = colours


