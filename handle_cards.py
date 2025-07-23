from property_set import PropertySet
from enums import FULL_SET_SIZES, PropertyColour

BDAY_DEBT = 2
DEBT = 5

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
        print("\nAvailable colours:")
        for i, colour in enumerate(valid_colours, start=1):
            
            print(f"{i}: {colour.name.replace('_', ' ').title()}")

        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice < len(valid_colours):
                    chosen_colour = valid_colours[choice]
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")

    # Two-colour wildcard
    else:
        print("\nChoose colour: ")
        for i, colour in enumerate(card.colours, start=1):
            print(f"{i}: {colour.name.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice < len(card.colours):
                    chosen_colour = card.colours[choice]
                    break
                else:
                    print("Invalid choice.")

            except ValueError:
                print("Please enter a number.")
            
    # Add property to dictionary
    if chosen_colour not in player.property_sets:
        player.property_sets[chosen_colour] = PropertySet(chosen_colour, FULL_SET_SIZES.get(chosen_colour, float('inf')))
    
    player.property_sets[chosen_colour].add_card(card)

    return

def handle_house_card(game, player, card):
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        print("You have no full sets to add a house.")
        return
        
    print("\nChoose a full property set to add a house:")
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
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        print("You have no full sets to add a hotel.")
        return
        
    print("\nChoose a full property set to add a hotel:")
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
    player.draw_cards(game.deck, 2)

def take_money(player, other, amount_due):
    print(f"{other.name}, you owe {player.name} ${amount_due}M.")
    print("Your bank:")
    for i, card in enumerate(other.bank, start=1):
        print(f"{i}: {card}")

    selected_indices = []
    total_given = 0

    while total_given < amount_due:
        choice = input(f"Select a card number to give (total given: ${total_given}M): ")
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(other.bank):
            print("Invalid card number.")
            continue
        if idx in selected_indices:
            print("Card already selected.")
            continue

        selected_indices.append(idx)
        total_given += other.bank[idx].value

        if total_given < amount_due:
            print(f"Total given so far is ${total_given}M. You still owe ${amount_due - total_given}M.")

    # Now remove the chosen cards in reverse order so indices don't shift
    selected_indices.sort(reverse=True)
    cards_given = []
    for idx in selected_indices:
        card = other.bank.pop(idx)
        cards_given.append(card)

    player.bank.extend(cards_given)

def handle_birthday_card(game, player, card):
    print(f"\n🎂 It's {player.name}'s Birthday! Every player must pay $2M.")
    
    for other in game.players:
        if other == player:
            continue

        if len(other.bank) == 0:
            print(f"{other.name} has no money to pay.")
            continue

        take_money(player, other, BDAY_DEBT)

def handle_debt_collector_card(game, player, card):
    print(f"\nChoose a player to pay $5M.")
    for i, other in enumerate(game.players, start=1):
        if other == player:
            continue
        print(f"{i}: {other}")
    
    for other in game.players:
        if other == player:
            continue

        if len(other.bank) == 0:
            print(f"{other.name} has no money to pay.")
            continue

        take_money(player, other, BDAY_DEBT)   
    