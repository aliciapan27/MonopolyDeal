from game_logic.enums import ActionType

ACTION_MESSAGES = {
    ActionType.HOUSE: {
        "intro": "\n🏠 Add a house to one of your full property sets.",
        "fail": "\nYou have no full sets to add a house."
    },
    ActionType.HOTEL: {
        "intro": "\n🏨 Add a hotel to one of your full property sets.",
        "fail": "\nYou have no full sets to add a hotel."
    },
    ActionType.PASS_GO: {
        "intro": "\n➡️ Pass Go! Draw 2 cards."
    },
    ActionType.BIRTHDAY: {
        "intro": "\n🎂 It's {player}'s Birthday!",
        "collect": "\nEveryone pays $2M to {player}.",
        "fail": "\n{target} has no money to pay."
    },
    ActionType.DEBT_COLLECTOR: {
        "intro": "\n💰 Debt Collector! {player}, force a player to pay you $5M.",
        "success": "\n{target} pays {player} $5M.",
        "fail": "\n{target} has no money to pay."
    },
    ActionType.FORCE_DEAL: {
        "intro": "\n🔁 Forced Deal! {player}, force a player to swap properties with you.",
        "fail1": "\nYou have no properties to trade.",
        "fail2": "\nNo other players have tradeable properties.",
        "wanted_card": "\nWhich one of {player}'s properties do you want?",
        "your_card": "Which one of your properties do you want to swap?"
    },
    ActionType.SLY_DEAL: {
        "intro": "\n🕵️ Sly Deal! {player}, choose a player to steal from.",
        "fail": "\nNo other players have stealable properties.",
        "wanted_card": "\nWhich one of {player}'s properties do you want?"
    },
    ActionType.RENT: {
        "colour_intro": "\n💸 Time to pay rent! {player}, choose a colour property.",
        "colour_collect": "\nEveryone pays {player} ${rent}M for {colour} properties!",
        "any_intro": "\n💸 Time to pay rent for! {player}, choose a colour property.",
        "choose_target": "\nForce a player to pay you ${rent}M for {colour} properties.",        
        "any_success": "\n {target} pays {player} ${rent}M.",
        "fail": "\n{target} has no money to pay.",
        "double": "\nYou have a Double the Rent card! Do you want to use it? (Y/N)"
    },
    ActionType.JUST_SAY_NO: {
        "intro": "\n❌ {player} played Just Say No!",
        "use_just_say_no": "\n{player}, you have a Just Say No! Do you want to use it? (Y/N)",
        "counter_no": "\n{collector}, you have a Just Say No! Do you want to counter {payer}'s Just Say No? (Y/N)"
    },
    ActionType.DOUBLE_RENT: {
        "intro": "\n🚨💰 {player} doubled the rent!"
    },
    ActionType.DEAL_BREAKER: {
        "intro": "\n💼💥 Deal Breaker! {player}, steal any full set!",
        "fail": "\nNo players have full sets to steal.",
        "wanted_card": "\nWhich one of {player}'s full sets' do you want?"
    },
    "prompt_payment": {
        "prompt": "\n{payer}, you owe ${amount_due}M.",
        "not_enough": "{payer} doesn't have enough money to pay the full amount.",
        "no_money": "{payer} has no more money in their bank."
    }
}