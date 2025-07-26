RESET_ACTIONS = 3

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bank = []

        self.property_sets = {}
        self.actions_remaining = 3 #reset each turn

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
            hand_st += f"{i}: {card}\n"
        return hand_st

    def choose_card(self):
        money_mode = False

        print(f"\n{self}")
        while True:
            self.print_hand()

            #choice = input("Enter the number of the card to play or 'm' for money mode (card chosen will be played as money) (or 'q' to quit): ")
            choice = input(
                "Choose an option:\n"
                "  - Enter the number of the card to play\n"
                "  -  Enter 'm' to switch to money mode (card will be played as money)\n"
                "  - Enter 'q' to end turn early\n"
                "Your choice: "
            ).strip().lower()
            
            if choice.lower() == 'q':
                return None, None, False

            if choice.lower() == 'm':
                print("Money mode activated: your next chosen card will be played as money.")
                money_mode = True
                continue

            if not choice.isdigit() or (int(choice)-1) not in range(len(self.hand)):
                print("Invalid choice. Try again.")
                continue

            card_index = int(choice)-1
            chosen_card = self.hand[card_index]
            print(f"\nYou chose {chosen_card.name}")
            return chosen_card, card_index, money_mode
            
    def draw_cards(self, deck, count):
        drawn_cards = []
        for _ in range(count):
            if deck:
                card = deck.pop()
                self.hand.append(card)
                drawn_cards.append(card)
            else:
                print("Deck is empty! Cannot draw more cards.")

        if drawn_cards:
            print("You drew: ")
            for card in drawn_cards:
                print(f"- {card}")

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
