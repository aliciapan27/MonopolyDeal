from enums import ActionType

ACTION_MESSAGES = {
    ActionType.HOUSE: {
        "intro": "\n🏠 Add a house to one of your full property sets."
    },
    ActionType.HOTEL: {
        "intro": "\n🏨 Add a hotel to one of your full property sets."
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
        "intro": "\n💰 Debt Collector! {player}, choose a player to demand $5M from.",
        "success": "\n{target} pays {player} $5M.",
        "fail": "\n{target} has no money to pay."
    }
}