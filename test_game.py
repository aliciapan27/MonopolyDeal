from game_logic.game import Game
from game_logic.player import Player
from game_logic.deck import create_test_hand1, create_test_hand2

def main():
    
    # print_deck_info(deck)
    # print_full_deck(deck)

    # Game in 1 player test mode
    alicia = Player("Alicia")
    james = Player("James")
    players = [alicia, james]
    game = Game(players)
    game.start()

    #give test hands
    alicia.hand = create_test_hand1()
    james.hand = create_test_hand2()

    #game loop
    current_player_index = 0

    for turn in range(5):  # Replace with a better game-over condition later
        current_player = players[current_player_index]
        print(f"\n--- {current_player.name}'s Turn ---")

        game.take_turn(current_player)

        # Toggle to next player
        current_player_index = (current_player_index + 1) % len(players)


    

    

if __name__ == "__main__":
    main()