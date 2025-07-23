from deck import create_deck, shuffle_deck, print_deck_info, print_full_deck
from player import Player
from game import Game

def main():
    # deck = create_deck()
    # shuffle_deck(deck)
    # print_deck_info(deck)
    # print_full_deck(deck)

    # Game in 1 player test mode
    player = Player("Alicia")
    game = Game(player, test_mode=True)

    game.start()
    player.start_turn()

    

    

if __name__ == "__main__":
    main()