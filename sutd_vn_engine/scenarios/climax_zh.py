"""Zhao Hui's Climax Scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = ["event_friend_intruder", "event_persuade_friend", "event_intruder"]


def event_friend_intruder(G: Controller):
    """Intruder alert to idol hotel."""
    G.set_speaker("ai", "left")
    G.print(
        "You met up with your Johnathan who is also a huge fan of JH."
        "Johnathan: Hey ! I found out which hotel JH will be staying at."
        "Johnathan: I am thinking of breaking into his room to ask for a picture.."
        "Johnathan: You should follow me along !"
    )

    while G.flags_dict.get("BREAK_INTO_HOTEL") is None:
        # TRIGGER GAME
        reply = G.input(
            f"So {G.flags_dict['USERNAME']}, Do you want to join Johnathan on his adventure?"
        )
        reply = reply.lower()
        if reply[0] == "y":
            G.flags_dict["BREAK_INTO_HOTEL"] = True
        elif reply[0] == "n":
            G.flags_dict["BREAK_INTO_HOTEL"] = False

    if G.flags_dict["BREAK_INTO_HOTEL"]:
        G.print("LETS BREAK INTO HIS ROOM ! LET'S GO !!!")
    else:
        G.print("Hmmm that sounds hella illegal. I think its a really bad idea.")
        G.set_speaker("ai", "left")


def event_persuade_friend(G: Controller):
    """Intruder alert to idol hotel."""
    G.set_speaker("ai", "left")
    G.print("You rejected your friend's offer to break into JH's hotel room.")

    while G.flags_dict.get("PERSUADE_FRIEND") is None:
        # TRIGGER GAME
        reply = G.input(
            f"So {G.flags_dict['USERNAME']}, Do you want to dissuade Johnathan from breaking in?"
            "If yes, key in Y"
            "Or Do you want to let Johnathan break into JH's room?"
            "Key in N"
        )
        reply = reply.lower()
        if reply[0] == "y":
            G.flags_dict["PERSUADE_FRIEND"] = True
        elif reply[0] == "n":
            G.flags_dict["PERSUADE_FRIEND"] = False

    if G.flags_dict["PERSUADE_FRIEND"]:
        G.print(
            "Hey Johnathan. I think this is a really bad idea."
            "You shouldn't be breaking in to other people's room."
            "Please don't do this."
            "You will get into trouble for this."
        )
    else:
        G.print(
            "Hmmm that sounds hella illegal. I think its a really bad idea."
            "But hey it's not me that is doing it."
            "Johnathan can do whatever he wants."
            "I'll just ask him to help me get a signature from Songhyun."
        )
        G.set_speaker("ai", "left")


def event_intruder(G: Controller):
    """Intruder alert to idol house."""
    if not G.flags_dict.get("BREAK_INTO_HOTEL"):
        return

    G.set_speaker("ai", "left")
    G.print(
        "As you creep towards your JH's room, you hear a noise coming from the room."
        "Your heart is beating very quickly !!!!  "
        "You wonder what JH is doing in the room."
        "You tried turning the door knob... but you realised it is locked."
    )

    while G.flags_dict.get("GAME_WIN") is None:
        if G.flags_dict.get("GAME_WIN") is True:
            G.print(
                "You figured out the passcode for the door."
                "You: I'm so nervous !!!!!!!!!"
                "You: I can't believe I'm finally able to meet JH face to face"
                "You slowly turn the door knob...."
                "You hear an unfamiliar voice in the room..."
                "You peek into the room and you see something that you are not supposed to see..."
                "You see a girl on top of JH on the bed..."
            )

        elif G.flags_dict.get("GAME_WIN") is False:
            G.print(
                "You couldn't figure out the passcode for the door."
                "You hear the door being unlocked"
                "You: I can't believe I'm finally able to meet JH face to face"
                "The door knob slowly turns...."
                "You peek into the room and you see JH..."
                "AHHHHHH !!!! WHO ARE YOU !? "
                "YOU JUST GOT CAUGHT TRYING TO BREAK INTO YOUR JH'S ROOM"
            )


lower_bound = 000
upper_bound = 999
max_attempts = 3
birthday = 201


def get_guess():
    while True:
        try:
            guess = int(
                G.input(f"Guess the passcode between {lower_bound} and {upper_bound}: ")
            )
            if lower_bound <= guess <= upper_bound:
                return guess
            else:
                G.print(
                    "Invalid input. Please enter a number within the specified range."
                )
        except ValueError:
            G.print("Invalid input. Please enter a valid number.")


# Validate guess
def check_guess(guess, birthday):
    if guess == birthday:
        G.flags_dict["GAME_WIN"] = True
        return "Correct"
    elif guess < birthday:
        return "Too low"
    else:
        return "Too high"


# track the number of attempts, detect if the game is over
def play_game(G: Controller):
    attempts = 0
    won = False

    while attempts < max_attempts:
        attempts += 1
        guess = get_guess()
        result = check_guess(guess, birthday)

        if result == "Correct":
            G.print(f"Awesome ! You managed to figure out the passcode to JH's room.")
            won = True
            break
        else:
            G.print(f"{result}. Try again!")

    if not won:
        print(
            f"You have used up your 3 tries."
            "You failed to break into JH's room."
            "As a result, you alerted JH and he called security on you."
            "You have been arrested for trespassing...."
        )
        G.flags_dict["GAME_WIN"] = False


if __name__ == "__main__":
    G.print("Welcome to the Number Guessing Game!")
    play_game()
