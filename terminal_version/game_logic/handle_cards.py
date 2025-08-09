from game_logic.property_set import PropertySet
from game_logic.enums import PropertyColour, ActionType
from game_logic.card_data import FULL_SET_SIZES
from game_logic.messages import ACTION_MESSAGES

BDAY_DEBT = 2
DEBT = 5

#Helper functions
def prompt_colour_choice(game, player, colours):
    game.send_message(player, "Choose a property colour:")
    options_text = "\n".join(f"{i}: {colour.name.title()}" 
                             for i, colour in enumerate(colours, start=1))
    game.send_message(player, options_text)

    while True:
        try:
            colour_choice = game.prompt_player(player, "Enter the number of your choice: ")
            index = int(colour_choice) -1
            if 0 <= index < len(colours):
                return colours[index]
            else:
                game.send_message(player, "❌ Invalid choice. Try again.")
        except ValueError:
            game.send_message(player, "Please enter a number.")
        
def prompt_player_choice(game, player, target_players):
    game.send_message(player, "Choose a player:")
    options_text = "\n".join(f"{i}: {other}" 
                             for i, other in enumerate(target_players, start=1))
    game.send_message(player, options_text)

    while True:
        try:
            choice = game.prompt_player(player, "Enter the number of your choice: ")
            index = int(choice) -1
            if 0 <= index < len(target_players):
                return target_players[index]
            else:
                game.send_message(player, "Invalid choice.")
        except ValueError:
            game.send_message(player, "Please enter a number.")

def prompt_property_choice(game, player, properties):
    game.send_message(player,"\nChoose a property:")

    options_text = "\n".join(f"{i}: {property.name}" 
                             for i, property in enumerate(properties, start=1))
    game.send_message(player, options_text)

    while True:
        try:
            choice = game.prompt_player(player, "Enter the number of your choice: ")
            index = int(choice) -1
            if 0 <= index < len(properties):
                return properties[index]
            else:
                game.send_message(player, "Invalid choice.")

        except ValueError:
            game.send_message(player, "Please enter a number.")

def prompt_full_set_choice(game, player, full_sets):
    game.send_message(player,"\nChoose a full set:")
    options_text = "\n".join(f"{i}: {str(property)}" 
                             for i, property in enumerate(full_sets, start=1))
    game.send_message(player, options_text)
            
    while True:
        try:
            choice = game.prompt_player(player, "Enter the number of your choice: ")
            index = int(choice) -1
            if 0 <= index < len(full_sets):
                return full_sets[index]
            else:
                game.send_message(player, "Invalid choice.")

        except ValueError:
            game.send_message(player, "Please enter a number.")

def try_just_say_no(game, attacker, defender):
    message = ACTION_MESSAGES[ActionType.JUST_SAY_NO]
    #Check if player has just say no
    for card in defender.hand:
        if card.action_type == ActionType.JUST_SAY_NO:
            response = input(message["use_just_say_no"].format(player = defender.name) + " ").strip().lower()
            
            if response == "y":
                handle_just_say_no_card(game, defender, card)

                #Check if attacker has a just say no to play
                if try_just_say_no(game, defender, attacker):
                    game.broadcast(f"{attacker.name}'s Just Say No cancels {defender.name}'s Just Say No.")
                    return False #original just say no blocked
                else:
                    return True #action blocked successfully
    return False #no just say no played

def prompt_payment(game, payer, collector, amount_due):
    message = ACTION_MESSAGES["prompt_payment"]

    if try_just_say_no(game, collector, payer):
        return None

    selected_indices = []
    total_given = 0

    game.send_message(payer, message["prompt"].format(payer=payer.name, amount_due=amount_due))

    while total_given < amount_due:
        remaining_cards = [c for i, c in enumerate(payer.bank) if i not in selected_indices]

        if not remaining_cards:
            game.broadcast(message["no_money"].format(payer=payer.name))
            break

        # Show current bank
        bank_string = "Your bank:\n"
        for i, card in enumerate(payer.bank, start=1):
            if i - 1 in selected_indices:
                continue
            bank_string += f"{i}: {card}\n"

        bank_string += f"\n💰 Total given so far: ${total_given}M"
        if total_given < amount_due:
            bank_string += f"\nYou still owe: ${amount_due - total_given}M"

        # Prompt player
        choice = game.prompt_player(payer, bank_string + "\nSelect a card number to give:")

        if not choice.isdigit():
            game.send_message(payer, "Please enter a valid number.")
            continue

        money_choice = int(choice) - 1
        if money_choice < 0 or money_choice >= len(payer.bank):
            game.send_message(payer, "Invalid card number.")
            continue
        if money_choice in selected_indices:
            game.send_message(payer, "Card already selected.")
            continue

        selected_indices.append(money_choice)
        total_given += payer.bank[money_choice].value

    selected_indices.sort(reverse=True)
    return [payer.bank.pop(i) for i in selected_indices]

def collect_payment(game, collector, payer, amount):
        if len(payer.bank) == 0:
            game.broadcast("{payer.name} has no money to pay.")
            return False

        cards_given = prompt_payment(game, payer, collector, amount)

        if cards_given is None:
            game.broadcast(f"{payer.name} used 'Just Say No' to block the payment.")
            return False
        
        collector.bank.extend(cards_given)
        return True

def players_with_tradeable(game, player):
    players_with_tradeables = []

    for other in game.players:
        if other == player:
            continue

        tradeable_sets = other.get_tradeable_properties()

        if tradeable_sets:
            players_with_tradeables.append(other)

    return players_with_tradeables

def players_with_full_sets(game, player):
    players_with_full_sets = []

    for other in game.players:
        if other == player:
            continue

        full_sets = other.get_full_sets()

        if full_sets:
            players_with_full_sets.append(other)

    return players_with_full_sets

#Action card Handlers
def handle_money_card(game, player, card):
    player.bank.append(card)
    return True

def handle_property_card(game, player, card):
    if card.colour not in player.property_sets:
        player.property_sets[card.colour] = PropertySet(card.colour, FULL_SET_SIZES.get(card.colour, float('inf')))
    player.property_sets[card.colour].add_card(card)
    return True
    
def handle_wildcard(game, player, card):
    # Universal wildcard
    if card.colours[0] == PropertyColour.ANY:
        valid_colours = [colour for colour in PropertyColour if colour != PropertyColour.ANY]
        chosen_colour = prompt_colour_choice(game, player, valid_colours)

    # Two-colour wildcard
    else:
        valid_colours = card.colours
        chosen_colour = prompt_colour_choice(game, player, valid_colours)
    
    #set wildcard colour
    card.colour = chosen_colour
    # Add property to dictionary
    if chosen_colour not in player.property_sets:
        player.property_sets[chosen_colour] = PropertySet(chosen_colour, FULL_SET_SIZES.get(chosen_colour, float('inf')))
    
    player.property_sets[chosen_colour].add_card(card)
    return True

def handle_house_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.HOUSE]
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        game.broadcast(message["fail"])
        return False
        
    game.send_message(player, message["intro"])
    
    for i, prop_set in enumerate(full_sets, start = 1):
        card_names = ', '.join(card.name for card in prop_set.cards)
        game.send_message(player, f"{i}. {prop_set.colour.name.title()} ({card_names})")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(full_sets):
                chosen_set = full_sets[choice]
                break
            else:
                game.send_message(player,"Invalid choice. Try again.")

        except ValueError:
            game.send_message(player, "Please enter a number.")

    # Add house to set
    chosen_set.add_house()
    return True

def handle_hotel_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.HOTEL]
    full_sets = [prop_set for prop_set in player.property_sets.values() 
                    if prop_set.is_full]
        
    if not full_sets:
        game.send_message(player,message["fail"])
        return False
        
    game.send_message(player, message["intro"])
    for i, prop_set in enumerate(full_sets, start = 1):
        card_names = ', '.join(card.name for card in prop_set.cards)
        game.send_message(player, f"{i}. {prop_set.colour.name.title()} ({card_names})")

    while True:
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if 0 <= choice < len(full_sets):
                chosen_set = full_sets[choice]
                break
            else:
                game.send_message(player,"Invalid choice. Try again.")

        except ValueError:
            game.send_message(player,"Please enter a number.")

    # Add hotel to set
    chosen_set.add_hotel()
    return True

def handle_pass_go_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.PASS_GO]
    game.send_message(player, message["intro"])
    player.draw_cards(game.deck, 2)
    return True

def handle_birthday_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.BIRTHDAY]
    game.broadcast(message["intro"].format(player = player.name))
    game.broadcast(message["collect"].format(player = player.name))

    #Everyone pays
    for other in game.players:
        if other == player:
            continue
        collect_payment(game, player, other, BDAY_DEBT)
    return True
    
def handle_debt_collector_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.DEBT_COLLECTOR]
    game.send_message(player, message["intro"])
    
    target_players = [p for p in game.players if p != player]
    chosen_player = prompt_player_choice(game, player, target_players)
    collect_payment(game, player, chosen_player, DEBT)
    return True

def handle_force_deal_card(game, player, card): 
    message = ACTION_MESSAGES[ActionType.FORCE_DEAL]

    #player has no properties to trade
    if not player.property_sets:
        game.send_message(player, message["fail1"])
        return False
    
    target_players =  players_with_tradeable(game, player)

    #no other players have properties to trade
    if not target_players:
        game.send_message(player, message["fail2"])
        return False

    game.send_message(player, message["intro"])
    
    #choose player to trade with
    chosen_player = prompt_player_choice(game, player, target_players)

    #choose property to trade with
    game.send_message(player, message["wanted_card"].format(player=chosen_player.name))
    wanted_card = prompt_property_choice(game, player, chosen_player.get_tradeable_properties())
    
    game.send_message(player, message["your_card"])
    card_to_swap = prompt_property_choice(game, player, player.get_tradeable_properties())
    
    #remove cards from set
    chosen_player.property_sets[wanted_card.colour].remove_card(wanted_card)
    player.property_sets[card_to_swap.colour].remove_card(card_to_swap)

    #add cards to new sets
    if card_to_swap.colour not in chosen_player.property_sets:
        chosen_player.property_sets[card_to_swap.colour] = PropertySet(card_to_swap.colour, FULL_SET_SIZES.get(card_to_swap.colour, float('inf')))
    chosen_player.property_sets[card_to_swap.colour].add_card(card_to_swap)

    if wanted_card.colour not in player.property_sets:
        player.property_sets[wanted_card.colour] = PropertySet(wanted_card.colour, FULL_SET_SIZES.get(wanted_card.colour, float('inf')))
    player.property_sets[wanted_card.colour].add_card(wanted_card)

    return True

def handle_sly_deal_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.SLY_DEAL]
    
    target_players =  players_with_tradeable(game, player)

    #no other players have properties to steal from
    if not target_players:
        game.send_message(player,message["fail"])
        return False

    game.send_message(player, message["intro"])
    
    #choose player to steal from
    chosen_player = prompt_player_choice(game, player, target_players)

    #choose property to steal
    game.send_message(player, message["wanted_card"].format(player=chosen_player.name))
    wanted_card = prompt_property_choice(game, player, chosen_player.get_tradeable_properties())
    
    #remove card from set
    chosen_player.property_sets[wanted_card.colour].remove_card(wanted_card)
    
    if wanted_card.colour not in player.property_sets:
        player.property_sets[wanted_card.colour] = PropertySet(wanted_card.colour, FULL_SET_SIZES.get(wanted_card.colour, float('inf')))
    player.property_sets[wanted_card.colour].add_card(wanted_card)

    return True

def handle_rent_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.RENT]

    #Colour rent card
    if card.colours[0] != PropertyColour.ANY:
        valid_colours = card.colours
        #Choose colour
        game.send_message(player, message["colour_intro"])
        chosen_colour = prompt_colour_choice(game, player, valid_colours)

        rent = player.property_sets[chosen_colour].rent

        #Check if player has double rent card
        for card in player.hand:
            if card.action_type == ActionType.DOUBLE_RENT and player.actions_remaining > 1:
                response = input(message["double"] + " ").strip().lower()
                
                if response == "y":
                    handle_double_rent_card(game, player, card)
                    rent *= 2
        
        game.broadcast(message["colour_collect"].format(player = player.name, colour = chosen_colour.name.title(), rent = rent))
    
        #Everyone pays
        for other in game.players:
            if other == player:
                continue
            collect_payment(game, player, other, rent)
    #ANY rent card
    else:
        valid_colours = [colour for colour in PropertyColour if colour != PropertyColour.ANY]
        #Choose colour
        game.send_message(player, message["colour_intro"])
        chosen_colour = prompt_colour_choice(game, player, valid_colours)

        rent = player.property_sets[chosen_colour].rent

        #Check if player has double rent card
        for card in player.hand:
            if card.action_type == ActionType.DOUBLE_RENT and player.actions_remaining > 1:
                response = input(message["double"] + " ").strip().lower()
                
                if response == "y":
                    handle_double_rent_card(game, player, card)
                    rent *= 2
    
        #Choose player
        game.send_message(player, message["choose_target"].format(player = player.name, colour = chosen_colour.name.title(), rent = rent))
        target_players = [p for p in game.players if p != player]
        chosen_player = prompt_player_choice(game, player, target_players)
        
        collect_payment(game, player, chosen_player, rent)
    return True

def handle_just_say_no_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.JUST_SAY_NO]
    game.broadcast(message["intro"].format(player = player.name))
    #discard card
    game.discard_card(player, card)
    return True

def handle_deal_breaker_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.DEAL_BREAKER]
    
    target_players =  players_with_full_sets(game, player)

    #no other players have properties to steal from
    if not target_players:
        game.send_message(player, message["fail"])
        return False

    game.send_message(player, message["intro"].format(player = player.name))
    
    #choose player to steal from
    chosen_player = prompt_player_choice(game, player, target_players)

    #choose property to steal
    game.send_message(player, message["wanted_card"].format(player=chosen_player.name))
    wanted_set = prompt_full_set_choice(game, player, chosen_player.get_full_sets())
    
    #remove full set
    del chosen_player.property_sets[wanted_set.colour]
    
    if wanted_set.colour not in player.property_sets:
        player.property_sets[wanted_set.colour] = wanted_set 
        #doenstr handle if you already have a property in this colur
    
    
    return True

def handle_double_rent_card(game, player, card):
    message = ACTION_MESSAGES[ActionType.DOUBLE_RENT]
    game.broadcast(message["intro"].format(player = player.name))
    return True
