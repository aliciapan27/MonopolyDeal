from card_data import PROPERTY_RENT

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
    
    def __str__(self):
        status = "✅" if self.is_full else ""
        card_names = ", ".join(card.name for card in self.cards)
        return (
            f"  {self.colour.name.title()}{status} "
            f"(🏠 {self.house_count}, 🏨 {self.hotel_count}, 💰 {self.rent}): "
            f"{card_names}"
        )

    def check_if_full(self):
        return len(self.cards) >= self.required_size

    def add_card(self, card):
        self.cards.append(card)
        self.is_full = self.check_if_full()
        self.update_rent()
    
    def remove_card(self, card):
        self.cards.remove(card)
        self.is_full = self.check_if_full()
        self.update_rent()
    
    def add_house(self):
        self.house_count += 1
        
    def add_hotel(self):
        self.hotel_count += 1
        self.update_rent()

    def update_rent(self):
        if not self.cards:
            self.rent = 0
            return
        
        rent_table = PROPERTY_RENT[self.colour]
        property_count = len(self.cards)
        index = min(property_count, len(rent_table))-1

        base_rent = rent_table[index]
        self.rent = base_rent + self.house_count*HOUSE_RENT + self.hotel_count*HOTEL_RENT

