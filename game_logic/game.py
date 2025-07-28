from game_logic.deck import create_deck, shuffle_deck
from game_logic.card import *
from game_logic.handle_cards import *

import threading

STARTING_HAND = 5
DRAW_TWO = 2
STARTING_ACTIONS = 3

class Game:
    def __init__(self, players, shutdown_event, send_message_func, broadcast_func, prompt_player_func):
        self.players = players
        self.discard_pile = []
        self.current_player_index = 0

        self.game_over = False
        self.curr_turn = 0

        self.shutdown_event = shutdown_event
        self.send_message = send_message_func
        self.broadcast = broadcast_func
        self.prompt_player = prompt_player_func
        # self.set_active_player = set_active_player_func
        # self.end_game = end_game_func

        self.deck = create_deck()

    def msg_drawn_cards(self, player, cards):
        if cards:
            message = "You drew:\n" + "\n".join(f"- {card}" for card in cards)
        else:
            message = "Deck is empty! You couldn't draw any cards."

        self.send_message(player, message)

    def start(self):
        shuffle_deck(self.deck)
        self.broadcast("\n🎮 Game starting with two players!\n")

        # Deal 5 cards to each player
        for player in self.players:
            player.draw_cards(self.deck, STARTING_HAND)
            self.send_message(player, player.get_hand_string())

        print("[GAME] Sent initial hands to all players.\n")
        #self.game_loop()
        threading.Thread(target=self.game_loop, daemon=True).start()

    def game_loop(self):
        while not self.shutdown_event.is_set() and not self.game_over:
            current_player = self.players[self.curr_turn]
            self.send_message(current_player, "Your turn!\n")
            self.broadcast(f"\n🟢 {current_player.name}'s turn\n")

            self.take_turn(current_player)

            if self.game_over or self.shutdown_event.is_set():
                break

            self.curr_turn = (self.curr_turn + 1) % len(self.players)

    def take_turn(self, player):
        player.actions_remaining = STARTING_ACTIONS

        #Draw 2 cards to begin
        drawn_cards = player.draw_cards(self.deck, DRAW_TWO)
        self.msg_drawn_cards(player, drawn_cards)

        self.send_message(player, player.get_hand_string())
        self.send_message(player, "Enter 'q' to quit or 'x' to end your turn early.")

        while player.actions_remaining > 0 and not self.shutdown_event.is_set():
            choice = self.prompt_player(player, "Your move: ").strip().lower()

            if choice == 'q':
                self.broadcast(f"{player.name} quit the game.")
                self.end_game()
                return

            elif choice == 'x':
                self.broadcast(f"{player.name} entered x (ended their turn).")
                break

            else:
                self.send_message(player, f"You entered: {choice} (not implemented)")
    
    
    def choose_card(self):
        money_mode = False

        print(f"\n{self}")
        while True:
            self.print_hand()

            #choice = input("Enter the number of the card to play or 'm' for money mode (card chosen will be played as money) (or 'q' to quit): ")
            choice = input(
                "Choose an option:\n"
                "  - Enter the number of the card to play\n"
                "  - Enter 'm' to switch to money mode (card will be played as money)\n"
                "  - Enter 'x' to end turn early\n"
                "Your choice: "
            ).strip().lower()
            
            if choice.lower() == 'x':
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
        
    def discard_card(self, player, card):
        if card in player.hand:
            player.hand.remove(card)
        self.discard_pile.append(card)
    
    def play_as_money(self, player, card, card_index):
        success = handle_money_card(self, player, card)

        if success:
            player.hand.pop(card_index)
            player.actions_remaining -= 1
        
    def play_card(self, player, card, card_index):
        if isinstance(card, MoneyCard):
            success = handle_money_card(self, player, card)
        elif isinstance(card, PropertyCard):
            success = handle_property_card(self, player, card)
        elif isinstance(card, WildCard):
            success = handle_wildcard(self, player, card)
        elif isinstance(card, HouseCard):
            success = handle_house_card(self, player, card)
        elif isinstance(card, HotelCard):
            success = handle_hotel_card(self, player, card)
        elif isinstance(card, PassGoCard):
            success = handle_pass_go_card(self, player, card)
        elif isinstance(card, BirthdayCard):
            success = handle_birthday_card(self, player, card)
        elif isinstance(card, DebtCollectorCard):
            success = handle_debt_collector_card(self, player, card)
        elif isinstance(card, ForceDealCard):
            success = handle_force_deal_card(self, player, card)
        elif isinstance(card, SlyDealCard):
            success = handle_sly_deal_card(self, player, card)
        elif isinstance(card, RentCard):
            success = handle_rent_card(self, player, card)
        elif isinstance(card, JustSayNoCard):
            success = handle_just_say_no_card(self, player, card)
        elif isinstance(card, DealBreakerCard):
            success = handle_deal_breaker_card(self, player, card)
        elif isinstance(card, DoubleRentCard):
            success = False
            print("\nNeed to play rent card first!")
        
        else:
            success = False
            print("\nAction not implemented yet")

        #pop from hand
        if success:
            player.hand.pop(card_index)
            self.discard_card(player, card) #just say no cards are discarded in handle_cards.py

            #shouldn't discard money or properties, fix this later
            player.actions_remaining -= 1

    def end_game(self):
        self.broadcast(f"\n🛑 Game Over.")
        self.game_over = True
