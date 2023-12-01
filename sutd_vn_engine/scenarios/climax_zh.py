"""Zhao Hui's Climax Scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = [
    "event_friend_intruder",
    "event_persuade_friend",
    "event_intruder",
]


def event_friend_intruder(G: Controller):
    """Intruder alert to idol hotel."""
    if G.flags_dict.get("GAMEOVER"):
        return
    G.set_speaker("", "center")
    G.print("1 month later")
    G.set_speaker("Narrator", "left")
    G.print("You met up with your old friend, Johnathan who is also a huge fan of JH. ")
    G.set_speaker("Johnathan", "left")
    G.print("It's been so long since I've last seen you. ")
    G.set_speaker("You", "right")
    G.print(
        "Yeaa! The last time I saw you was back in Secondary School. "
        "What have you been up to?"
    )

    G.set_speaker("Johnathan", "left")
    G.print(
        "I was busy attending all of his world tour concerts and Meet and Greets. "
        "Been a huge fan since 2015 and atteneded every single concert. "
        "In 2016, his first world tour,\n2017 his first tour in England,\n2019 his tour in Japan. "
        "I just can't seem to get enough of him and his sweaty, hot body whenever perform. "
        "*Slurp"
    )

    G.set_speaker("You", "right")
    G.print(
        "Ohh me too !! I've recently been chasing him as well. I really like the way he is. "
        "I mean he is humble, good looking and talented. "
        "Anyway I have to go now... It was nice seeing you again. "
        "I have work at Lotte Sands tomorrow."
    )

    G.set_speaker("Johnathan", "left")
    G.print(
        "What a coincidence! I recently found out that JH will be staying there for his upcoming concert. "
        "I am thinking of breaking into his room to ask for a picture... (°͜ʖ°) "
        "You should follow me along! "
    )

    while G.flags_dict.get("BREAK_INTO_HOTEL") is None:
        # TRIGGER GAME
        reply = G.input(
            f"So {G.flags_dict['USERNAME']}, do you want to join Johnathan on his adventure? (y/n)"
        )
        reply = reply.lower()[:1]
        if reply == "y":
            G.flags_dict["BREAK_INTO_HOTEL"] = True
        elif reply == "n":
            G.flags_dict["BREAK_INTO_HOTEL"] = False
    G.set_speaker("You", "right")
    if G.flags_dict["BREAK_INTO_HOTEL"]:
        G.show_face("face_eldritch")
        G.print(
            "LETS BREAK INTO HIS ROOM! LET'S GET HIS BREAD!!! Σ(♡＠﹏ ＠☆)ﾉ "
            "Let's devise a plan to locate his room and meet him there. "
            "Since I am a janitor there, I have access to every building. "
            "How about you be the lookout and I try and figure out the door's passcode. "
            "Afterall, I know how the doorcodes work here."
        )
    else:
        G.print(
            "Hmmm that sounds hella illegal. I think its a really bad idea. (´⊙ω⊙`)！"
            "What if we get caught and go to jail?"
        )
        G.set_speaker("Narrator", "left")


def event_persuade_friend(G: Controller):
    """Intruder alert to idol hotel."""
    if G.flags_dict.get("GAMEOVER") or G.flags_dict.get("BREAK_INTO_HOTEL"):
        return
    G.set_speaker("Narrator", "left")
    G.print("You rejected your friend's offer to break into JH's hotel room. ಠ‿ಠ")
    G.show_face("face_obsessed1")
    while G.flags_dict.get("PERSUADE_FRIEND") is None:
        # TRIGGER GAME
        reply = G.input(
            f"So {G.flags_dict['USERNAME']}, Do you want to dissuade Johnathan from breaking in? "
            "If yes, key in Y "
            "Or Do you want to let Johnathan break into JH's room? "
            "Key in N "
        )
        reply = reply.lower()[:1]
        if reply == "y":
            G.flags_dict["PERSUADE_FRIEND"] = True
            G.show_face("face_sparkly")
        elif reply == "n":
            G.flags_dict["PERSUADE_FRIEND"] = False
            G.show_face("face_obsessed1")

    if G.flags_dict["PERSUADE_FRIEND"]:
        G.set_speaker("You", "right")
        G.print(
            "Hey Johnathan. I think this is a really bad idea. "
            "You shouldn't be breaking in to other people's room. "
            "Please don't do this. "
            "You will get into trouble for this. (；☉_☉) "
            "What if we get caught by the police for doing this. "
            "Although we are huge fans but this is totally out of this world. "
            "If you continue this behaviour, I will have to report you."
        )
    else:
        G.set_speaker("You", "right")
        G.print(
            "Hmmm that sounds hella illegal. I think its a really bad idea. "
            "But hey it's not me that is doing it. "
            "Johnathan can do whatever he wants. "
            "I'll just ask him to help me get a signature from JH. (づ ◕‿◕ )づ "
        )
        G.set_speaker("Narrator", "left")


def event_intruder(G: Controller):
    """Intruder alert to idol house."""
    if G.flags_dict.get("GAMEOVER"):
        return
    if not G.flags_dict.get("BREAK_INTO_HOTEL"):
        return

    G.set_speaker("Narrator", "left")
    G.print(
        "As you creep towards your JH's room, you hear a noise coming from the room. "
    )
    G.set_speaker("You", "right")
    G.print("Your heart is beating very quickly!!!!  ")
    G.print("You wonder what JH is doing in the room. ")
    G.print("You tried turning the door knob... but you realised it is locked. ⨀_⨀ ")
    G.print("┬┴┬┴┤ᵒᵏ (･_├┬┴┬┴")

    play_game(G)

    if G.flags_dict.get("GAME_WIN") is True:
        G.set_speaker("", "center")
        G.show_face("face_eldritch")
        G.print("You figured out the passcode for the door. ")
        G.set_speaker("You", "right")
        G.print("I'm so nervous!!!!!!!!!")
        G.print("I can't believe I'm finally able to meet JH face to face")

        G.set_speaker("Narrator", "left")
        G.print("You slowly turn the door knob... ")
        G.print("You hear an unfamiliar voice in the room... ")
        G.print(
            "You peek into the room and you see something that you are not supposed to see... "
        )
        G.print("You see a girl on top of JH on the bed... ⨀_⨀")

    elif G.flags_dict.get("GAME_WIN") is False:
        G.set_speaker("You", "right")
        G.print("Stupid door! (ノಠ益ಠ)ノ彡┻━┻ ")

        G.set_speaker("Narrator", "left")
        G.print("You hear the door being unlocked. ")
        G.print("You quickly hide behind the door. ")

        G.set_speaker("You", "right")
        G.print("I can't believe I'm finally able to meet JH face to face.")
        G.print("I'm so nervous!!!!!!!!! ")

        G.set_speaker("Narrator", "left")
        G.print("The door knob slowly turns.... ")
        G.print("You peek into the room and you see JH... ")

        G.set_speaker("JH", "left")
        G.print("AHHHHHH!!!! WHO ARE YOU!? (╬⓪益⓪) ")

        G.set_speaker("Narrator", "center")
        G.print("-You just got caught trying to break into JH's Room-")
        G.print("Game Over. You lose.")


lower_bound = 000
upper_bound = 999
max_attempts = 3
birthday = 201


def get_guess(G):
    G.set_speaker("", "center")
    while True:
        try:
            guess = int(
                G.input(
                    f"Guess the passcode between {lower_bound} and {upper_bound}:\n"
                    "Hint: JH's Birthday is on: 11/02/2002 "
                    "Use each digit once."
                )
            )
            if lower_bound <= guess <= upper_bound:
                return guess
            else:
                G.print(
                    "Invalid input. Please enter a number within the specified range. "
                )
        except ValueError:
            G.print("Invalid input. Please enter a valid number. ")


# Validate guess
def check_guess(G, guess, birthday):
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
        guess = get_guess(G)
        result = check_guess(G, guess, birthday)

        if result == "Correct":
            G.print(f"Awesome ! You managed to figure out the passcode to JH's room. ")
            won = True
            break
        else:
            G.print(f"Click clack, you input {guess} as the passcode...")
            G.print(f"{result}. Darn.")

    if not won:
        G.flags_dict["GAME_WIN"] = False


# if __name__ == "__main__":
#     print("Welcome to the Number Guessing Game!")
#     play_game()
