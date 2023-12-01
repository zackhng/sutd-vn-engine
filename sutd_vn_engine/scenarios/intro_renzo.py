"""Renzo's intro scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = ["event_intro", "event_bubble", "event_job"]


def event_intro(G: Controller):
    name = G.input("What is your name?")
    G.flags_dict["USERNAME"] = G.flags_dict["USERNAME"] if name == "" else name
    # Split very long text across multiple lines.
    G.set_speaker("You", "right")
    G.print("""Oh? who is he? JH...?""")
    G.print(
        "I have never really liked KPOP idols before, but he looks so handsome and tall."
        " He's so hot...!!! "
        "Imma be a fan of JH for life now!"
    )


def event_bubble(G: Controller):
    # TODO set score
    name = G.flags_dict["USERNAME"]

    G.set_speaker("Notification", "center")
    G.print("Connect with your favorite idols using Bubble")

    G.set_speaker("Prompt", "center")
    G.print("Would you like to download Bubble?")
    download_result = G.input("Type  Y/N")

    if download_result == "accept":
        G.set_speaker("You", "right")
        G.print(
            "Bubble?!"
            "A chatting app allows me to talk to my idols?"
            "Thats sensational! Let me try it now."
        )

        G.set_speaker("Notification", "center")
        G.print("Chat with JH now!")

        G.set_speaker("You", "right")
        G.print(
            "Hi JH ! I have been a fan of you for quite some time now. You are really amazing."
        )

        G.set_speaker("Notification", "center")
        G.print("""Message from JH""")

        G.set_speaker("JH", "left")
        G.print(
            "Hi {} ! I am glad that you like my songs, I am very grateful to have you as my fan".format(
                name
            )
        )

        G.set_speaker("Prompt", "center")
        reply = G.input("How will you reply?")

        G.set_speaker("You", "right")
        G.print(reply)

        G.set_speaker("Notification", "center")
        G.print("-End of conversation-")

        G.set_speaker("You", "right")
        G.print(
            "Awww... he is so kind" "Feels like i know him personally in real life…"
        )
    else:
        # TODO lead to boring route:
        pass


def event_job(G: Controller):
    G.set_speaker("Email Notification", "center")
    G.print("Message from Lotte Sands")

    G.set_speaker("Lotte Sands", "left")
    G.print(
        "Congratulations! We are giving you the opportunity to be a janitor for our hotel, Lotte Sands."
        "If you would like to accept please reply with Y, if not please reply with N."
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
            "Thank you for this opportunity! I will do my best to help the company."
        )
        G.set_speaker("Lotte Sands", "left")
        G.print("Great! See you at the office tomorrow.")
    else:
        G.print(
            "Thank you for taking the time to consider our job offer."
            "While we are disappointed to learn that you have decided to decline our offer,"
            "we completely understand and respect your decision."
        )
