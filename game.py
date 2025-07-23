from deck import create_deck, shuffle_deck, create_test_deck
from card import *
from handle_cards import *

STARTING_HAND = 5
DRAW_TWO = 2
RESET_ACTIONS = 3

class Game:
    def __init__(self, players, test_mode=False):
        self.players = players
        self.discard_pile = []
        self.current_player_index = 0
        self.test_mode = test_mode

        self.deck = create_deck()

    def start(self):
        #shuffle_deck(self.deck)

        # Deal 5 cards to each player

        if self.test_mode:
            self.players.hand = create_test_deck
        else:
            for player in self.players:
                player.draw_cards(self.deck, STARTING_HAND)


    def game_loop(self):
        while not self.check_win_condition():
            current_player = self.players[self.current_player_index]
            print(f"{current_player.name}'s turn")
            self.take_turn(current_player)
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def take_turn(self, player):
        print(f"\nCURRENT\n{player}")
        player.actions_remaining = 3
        player.draw_cards(self.deck, DRAW_TWO)

        while player.actions_remaining > 0:
            chosen_card = player.choose_card()

            if chosen_card is None:
                print("Turn ended.")
                break
        
            self.play_card(player, chosen_card)
            player.actions_remaining -= 1
        
    
    def play_card(self, player, card):
        if isinstance(card, MoneyCard):
            handle_money_card(self, player, card)
        elif isinstance(card, PropertyCard):
            handle_property_card(self, player, card)
        elif isinstance(card, WildCard):
            handle_wildcard(self, player, card)
        elif isinstance(card, HouseCard):
            handle_house_card(self, player, card)
        elif isinstance(card, HotelCard):
            handle_hotel_card(self, player, card)
        elif isinstance(card, PassGoCard):
            handle_pass_go_card(self, player, card)
        elif isinstance(card, BirthdayCard):
            handle_birthday_card(self, player, card)
        else:
            print("\nAction not implemented yet")

            


    def check_win_condition(self):
        for player in self.players:
            if player.has_won():
                print(f"{player.name} wins!")
                return True
        return False
