from game_logic.enums import CardType, ActionType

class Card:
    def __init__(self, name: str, card_type: CardType, value: int = 0, action_type = None):
        self.name = name
        self.card_type = card_type 
        self.value = value
        self.action_type = action_type

    def __str__(self):
        return f"{self.name} ({self.card_type}, ${self.value}M)"

# Money and property cards
class MoneyCard(Card):
    def __init__(self, value):
        super().__init__(f"${value}M", CardType.MONEY, value)

class PropertyCard(Card):
    def __init__(self, colour, name, full_set, value):
        super().__init__(name, CardType.PROPERTY, value)
        self.colour = colour
        self.full_set = full_set

    def __str__(self):
        return f"{self.name}, {self.colour}, Full set:{ self.full_set} ({self.card_type}, ${self.value}M)"
              
class WildCard(Card):
    def __init__(self, colours, value):
        name = f"{'/'.join(colour.name.replace('_', ' ').title() for colour in colours)} Wildcard"
        super().__init__(name, CardType.PROPERTY, value)
        self.colours = colours
        self.colour = None #not set yet

# Action cards
class HouseCard(Card):
    def __init__(self, value):
        super().__init__("House", CardType.ACTION, value, ActionType.HOUSE)

class HotelCard(Card):
    def __init__(self, value):
        super().__init__("Hotel", CardType.ACTION, value, ActionType.HOTEL)
        
class PassGoCard(Card):
    def __init__(self, value):
        super().__init__("PassGo", CardType.ACTION, value, ActionType.PASS_GO)
    
class BirthdayCard(Card):
    def __init__(self, value):
        super().__init__("It's My Birthday", CardType.ACTION, value, ActionType.BIRTHDAY)

class DebtCollectorCard(Card):
    def __init__(self, value):
        super().__init__("Debt Collector", CardType.ACTION, value, ActionType.DEBT_COLLECTOR)

class ForceDealCard(Card):
    def __init__(self, value):
        super().__init__("Force Deal", CardType.ACTION, value, ActionType.FORCE_DEAL)

class SlyDealCard(Card):
    def __init__(self, value):
        super().__init__("Sly Deal", CardType.ACTION, value, ActionType.SLY_DEAL)

class JustSayNoCard(Card):
    def __init__(self, value):
        super().__init__("Just Say No", CardType.ACTION, value, ActionType.JUST_SAY_NO)

class DealBreakerCard(Card):
    def __init__(self, value):
        super().__init__("Deal Breaker", CardType.ACTION, value, ActionType.DEAL_BREAKER)

class DoubleRentCard(Card):
    def __init__(self, value):
        super().__init__("Double Rent", CardType.ACTION, value, ActionType.DOUBLE_RENT)

# RENT CARDS
class RentCard(Card):
    def __init__(self, colours, value):
        name = f"{'/'.join(colour.name.replace('_', ' ').title() for colour in colours)} Rent"
        super().__init__(name, CardType.ACTION, value, ActionType.RENT)
        self.colours = colours


