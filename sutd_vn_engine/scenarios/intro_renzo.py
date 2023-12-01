"""Renzo's intro scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = ["event_intro", "event_bubble", "event_job"]


def event_intro(G: Controller):
    """Intro event."""
    G.set_speaker("Narrator", "left")
    G.show_face("face_sparkly")
    G.print("This is my first time seeing you. " "By the way, what is your name?")

    name = G.input("Input your name or leave blank.")
    G.flags_dict["USERNAME"] = G.flags_dict["USERNAME"] if name == "" else name
    G.print("Hi, {}! Make the right choices... ".format(G.flags_dict["USERNAME"]))
    G.print(
        "While browsing the internet one day, you stumbled across JH.  "
        "His defined facial features & smile immediately struck your heart. "
        "He looks exactly like your highschool crush but 10 times better. "
        "You decided to binge watch videos of him."
    )
    G.set_speaker("You", "right")
    G.print(f"Oh? who is he? JH...?")
    G.print(
        "I have never really liked KPOP idols before, but (｡・//ε//・｡) he looks so handsome and tall "
        "(♡°▽°♡) he's so hot...!!! "
        "(♡´艸`) I'm gonna be a fan of JH for life now!"
    )


def event_bubble(G: Controller):
    """Bubble event."""
    if G.flags_dict.get("GAMEOVER"):
        return

    # TODO set score
    name = G.flags_dict["USERNAME"]

    G.set_speaker("Notification", "center")
    G.print("Connect with your favorite idols using Bubble.")

    G.set_speaker("Prompt", "center")
    download_result = None

    while download_result is None:
        download_result = G.input("Do you accept the terms & conditions? (y/n)")
        download_result = download_result.lower()[:1]
        if download_result != "y" and download_result != "n":
            download_result = None

    if download_result == "y":
        G.show_face("face_interested")
        G.set_speaker("You", "right")
        G.print(
            "（ΦωΦ）Bubble?! "
            "A chatting app allows me to talk to my idols? (o・┏ω┓・o) "
            "Thats sensational! Let me try it now. "
        )

        G.set_speaker("Notification", "center")
        G.print("Chat with JH now!")

        G.set_speaker("You", "right")
        G.print(
            "Hi JH (๑ˊ͈ ॢꇴ ˋ͈)〜♡॰ॱ! I have been a fan of you for quite some time now. You are really amazing! "
        )

        G.set_speaker("Notification", "center")
        G.print("""Message from JH""")

        G.set_speaker("JH", "left")
        G.print(
            "Hi {}! I am glad that you like my songs, I am very grateful to have you as my fan. ".format(
                name
            )
        )

        G.set_speaker("Prompt", "center")
        reply = G.input("How will you reply?")

        G.set_speaker("You", "right")
        G.print(reply)

        G.set_speaker("JH", "left")
        G.print("... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...")

        G.set_speaker("Notification", "center")
        G.print("-End of conversation-")

        G.set_speaker("You", "right")
        G.print(
            "(≧▽≦) Kyaaaa... he is so kind. "
            "Feels like i know him personally in real life... "
        )
    else:
        G.flags_dict["GAMEOVER"] = True
        G.print("You have been banned from Bubble. Enjoy your boring life.")


def event_job(G: Controller):
    if G.flags_dict.get("GAMEOVER"):
        return

    G.set_speaker("Email Notification", "center")
    G.print("Message from Temp Job Agency")

    G.show_face("face_sparkly")
    G.set_speaker("Lotte Sands", "left")
    G.print(
        "Congratulations! We are giving you the opportunity to be a janitor for our hotel, Lotte Sands. "
        "If you would like to accept please reply with Y, if not please reply with N. "
    )

    while G.flags_dict.get("ACCEPT_JOB") is None:
        reply = G.input(f"So {G.flags_dict['USERNAME']}, do you accept the job (y/n)?")
        reply = reply.lower()[:1]
        if reply == "y":
            G.flags_dict["ACCEPT_JOB"] = True
        elif reply == "n":
            G.flags_dict["ACCEPT_JOB"] = False

    if G.flags_dict["ACCEPT_JOB"]:
        G.set_speaker("You", "right")
        G.print(
            "Thank you for this opportunity! I will do my best to help the company. "
        )
        G.set_speaker("Lotte Sands", "left")
        G.print("Great! See you at the office tomorrow. ")
        G.set_speaker("Narrator", "left")
        G.print("You are now a JANITOR at Lotte Sands. You are also a fan of JH. ")
    else:
        G.print(
            "Thank you for taking the time to consider our job offer. "
            "While we are disappointed to learn that you have decided to decline our offer, "
            "we completely understand and respect your decision. "
        )
        G.flags_dict["GAMEOVER"] = True
