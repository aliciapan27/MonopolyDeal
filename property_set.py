HOUSE_RENT = 3
HOTEL_RENT = 4

class PropertySet:
    def __init__(self, colour, required_size):
        self.colour = colour
        self.cards = []
        self.required_size = required_size

        self.is_full = False
        self.house_count = 0
        self.hotel_count = 0
        self.rent = 0

    def check_if_full(self):
        return len(self.cards) >= self.required_size

    def add_card(self, card):
        self.cards.append(card)
        self.is_full = self.check_if_full()
    
    def add_house(self):
        self.house_count += 1
        self.rent += HOUSE_RENT

    def add_hotel(self):
        self.hotel_count += 1
        self.rent += HOTEL_RENT


    def update_rent(self):
        # Optional: calculate based on card count or use a predefined table
        return len(self.cards) * 1_000  # Example logic
