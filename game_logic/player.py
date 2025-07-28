RESET_ACTIONS = 3

class Player:
    def __init__(self, name, conn = None):
        self.name = name
        self.hand = []
        self.bank = []

        self.property_sets = {}
        self.actions_remaining = 3 #reset each turn

        self.conn = conn

    def __str__(self):
        bank_str = ', '.join(f"${card.value}M" for card in self.bank)
    
        property_sets_str = "\n".join(
            str(prop_set) for prop_set in self.property_sets.values() if prop_set.cards
        ) 

        return (
            f"Player: {self.name}\n"
            f"Hand: {len(self.hand)} card(s)\n"
            f"Bank: [{bank_str}]\n"
            f"Property Sets:\n{property_sets_str}\n"
            f"Actions Remaining: {self.actions_remaining}"
        )
    
    def print_hand(self):
        print("\nYour hand:")
        for i, card in enumerate(self.hand, start=1):
            print(f"{i}: ", card)

    #for server
    def get_hand_string(self):
        hand_str = "\nYour hand:\n"
        for i, card in enumerate(self.hand, start=1):
            hand_str += f"{i}: {card}\n"
        return hand_str
            
    def draw_cards(self, deck, count):
        drawn_cards = []
        for _ in range(count):
            if deck:
                card = deck.pop()
                self.hand.append(card)
                drawn_cards.append(card)
            else:
                # print("Deck is empty! Cannot draw more cards.")
                break #no more cards

        # if drawn_cards:
        #     print("You drew: ")
        #     for card in drawn_cards:
        #         print(f"- {card}")

        return drawn_cards

    def get_tradeable_properties(self):
        tradeables = []
        for prop_set in self.property_sets.values():
            if not prop_set.is_full:
                tradeables.extend(prop_set.cards)
        return tradeables
    
    def get_full_sets(self):
        full_sets = []
        for prop_set in self.property_sets.values():
            if prop_set.is_full:
                full_sets.append(prop_set)
        return full_sets
