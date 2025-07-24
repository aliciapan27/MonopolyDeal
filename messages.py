from enums import ActionType

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
    ActionType.RENT: {
        "colour_intro": "\n💸 Time to pay rent! {player}, choose a colour property.",
        "colour_collect": "\nEveryone pays {player} ${rent}M for {colour} properties!",
        "any_intro": "\n💸 Time to pay rent for! {player}, choose a colour property.",
        "choose_target": "\nForce a player to pay you ${rent}M for {colour} properties.",        
        "any_success": "\n {target} pays {player} ${rent}M.",
        "fail": "\n{target} has no money to pay."
    },
    ActionType.JUST_SAY_NO: {
        "intro": "❌ \n{player} played Just Say No!"
    },
    "prompt_payment": {
        "use_just_say_no": "\nYou have a Just Say No! Do you want to use it? (Y/N)",
        "prompt": "\n{payer}, you owe ${amount_due}M.",
        "not_enough": "{payer} doesn't have enough money to pay the full amount.",
        "no_money": "{payer} has no more money in their bank."
    }
}