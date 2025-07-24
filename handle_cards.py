from property_set import PropertySet
from enums import PropertyColour, ActionType
from card_data import FULL_SET_SIZES
from messages import ACTION_MESSAGES

BDAY_DEBT = 2
DEBT = 5

#Helper functions
def prompt_colour_choice(colours):
    print("Choose a property colour:")
    for i, colour in enumerate(colours, start=1):
            print(f"{i}: {colour.name.title()}")
    while True:
        try:
            colour_choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= colour_choice < len(colours):
                return colours[colour_choice]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
        
def prompt_player_choice(target_players):
    print("Choose a player:")
    for i, other in enumerate(target_players, start=1):
        print(f"{i}: {other}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(target_players):
                return target_players[choice]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")

def prompt_payment(payer, amount_due):
    print(f"{payer.name}, you owe ${amount_due}M.")
    print("Your bank:")
    for i, card in enumerate(payer.bank, start=1):
        print(f"{i}: {card}")

    selected_indices = []
    total_given = 0

    while total_given < amount_due:
        choice = input(f"Select a card number to give (total given: ${total_given}M): ")
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(payer.bank):
            print("Invalid card number.")
            continue
        if idx in selected_indices:
            print("Card already selected.")
            continue

        selected_indices.append(idx)
        total_given += payer.bank[idx].value

        if total_given < amount_due:
            print(f"Total given so far is ${total_given}M. You still owe ${amount_due - total_given}M.")

    # remove the chosen cards in reverse order so indices don't shift
    selected_indices.sort(reverse=True)
    return [payer.bank.pop(i) for i in selected_indices]

def collect_payment(collector, payer, amount):
        if len(payer.bank) == 0:
            print(f"{payer.name} has no money to pay.")
            return False

        cards_given = prompt_payment(payer, amount)
        collector.bank.extend(cards_given)
        return True

#Action card Handlers
def handle_money_card(game, player, card):
    player.bank.append(card)

def handle_property_card(game, player, card):
    if card.colour not in player.property_sets:
        player.property_sets[card.colour] = PropertySet(card.colour, FULL_SET_SIZES.get(card.colour, float('inf')))
    player.property_sets[card.colour].add_card(card)
    
def handle_wildcard(game, player, card):
    # Universal wildcard
    if card.colours[0] == PropertyColour.ANY:
        valid_colours = [colour for colour in PropertyColour if colour != PropertyColour.ANY]
        chosen_colour = prompt_colour_choice(valid_colours)

    # Two-colour wildcard
    else:
        valid_colours = card.colours
        chosen_colour = prompt_colour_choice(valid_colours)
            
    # Add property to dictionary
    if chosen_colour not in player.property_sets:
        player.property_sets[chosen_colour] = PropertySet(chosen_colour, FULL_SET_SIZES.get(chosen_colour, float('inf')))
    
    player.property_sets[chosen_colour].add_card(card)

    return

def handle_house_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.HOUSE]
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        print(message["fail"])
        return
        
    print(message["intro"])
    for i, prop_set in enumerate(full_sets, start = 1):
        card_names = ', '.join(card.name for card in prop_set.cards)
        print(f"{i}. {prop_set.colour.name.title()} ({card_names})")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(full_sets):
                chosen_set = full_sets[choice]
                break
            else:
                print("Invalid choice. Try again.")

        except ValueError:
            print("Please enter a number.")

    # Add house to set
    chosen_set.add_house()
    return

def handle_hotel_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.HOTEL]
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        print(message["fail"])
        return
        
    print(message["intro"])
    for i, prop_set in enumerate(full_sets, start = 1):
        card_names = ', '.join(card.name for card in prop_set.cards)
        print(f"{i}. {prop_set.colour.name.title()} ({card_names})")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(full_sets):
                chosen_set = full_sets[choice]
                break
            else:
                print("Invalid choice. Try again.")

        except ValueError:
            print("Please enter a number.")

    # Add hotel to set
    chosen_set.add_hotel()
    return

def handle_pass_go_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.PASS_GO]
    print(message["intro"])
    player.draw_cards(game.deck, 2)

def handle_birthday_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.BIRTHDAY]
    print(message["intro"].format(player = player.name))
    print(message["collect"].format(player = player.name))

    #Everyone pays
    for other in game.players:
        if other == player:
            continue
        collect_payment(player, other, BDAY_DEBT)
    
def handle_debt_collector_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.DEBT_COLLECTOR]
    print(message["intro"].format(player = player.name))
    
    target_players = [p for p in game.players if p != player]

    chosen_player = prompt_player_choice(target_players)
    collect_payment(player, chosen_player, DEBT)
    
def handle_force_deal_card(game, player, card):
    return

def handle_rent_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.RENT]

    #Colour rent card
    if card.colours[0] == PropertyColour.ANY:
        valid_colours = [colour for colour in PropertyColour if colour != PropertyColour.ANY]
        #Choose colour
        print(message["colour_intro"].format(player = player.name))
        chosen_colour = prompt_colour_choice(valid_colours)
    
        print(message["colour_collect"].format(player = player.name, colour = chosen_colour.name.title(), rent = rent))
        
        #Everyone pays
        for other in game.players:
            if other == player:
                continue
            collect_payment(player, other, rent)
    #ANY rent card
    else:
        print(message["any_intro"])
    

    # Step 2: Print intro message
    print(message["any_rent_intro"].format(player=player.name, colour=chosen_colour.name.title(), rent=5))

    # Step 3: Choose target
    target_players = [p for p in game.players if p != player]
    for i, other in enumerate(target_players, start=1):
        print(f"{i}: {other.name}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(target_players):
                chosen_player = target_players[choice]
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")

    # Step 4: Check payment
    if chosen_player.total_money() == 0:  # You may want to define total_money()
        print(message["any_rent_fail"].format(target=chosen_player.name, colour=chosen_colour.name.title()))
    else:
        print(message["any_rent_success"].format(
            target=chosen_player.name,
            player=player.name,
            rent=5,
            colour=chosen_colour.name.title()
        ))
        take_money(player, chosen_player, 5)
    

