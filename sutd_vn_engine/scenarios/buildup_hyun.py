"""Hyun's build up scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = ["event_social_media", "event_dox", "event_reacttosns"]


def event_social_media(G: Controller):
    """Example event."""
    # Set who is speaking, and on what side the chat bubble appears.
    # i.e., "left", "right", or "center".
    G.set_speaker("News", "left")

    G.print(
        "*BREAKING* JH HAS BEEN DATING?!?!!"
        "JH has been reportedly dating a fan for several years. "
        "Since last year, many of JH fans had suspected as such, "
        "posting on forums and fan sites images of ‘JH Dating Ordinary Person’ evidence. "
        "The ‘evidence’ includes pictures of the two of them together, "
        "looking at each other lovingly, the two with couple items "
    )
    # Split very long text across multiple lines.
    G.set_speaker("You", "right")
    G.print(
        "Hm?"
        "JH is dating?? Thats ridiculous. "
        "He is loyal to his fans and to his fans only. "
        "No one should believe this kind of stupid rumours. "
        "I like my Idol JH and thus I trust him. I should maintain my stance as a fan."
    )
    G.print(
        "JH is going have his world tour soon… "
        "I hope this rumour doesn't ruin his feelings before his performance. "
        "I should look into the comments if there is any comments that may possibly hurt him. "
    )
    G.set_speaker("Haters", "left")
    G.print(
        "Ew.. what kind of idol is he?"
        "Can't believe he betrayed all his fans…"
        "Very disappointing. Quit Your job as an Idol"
    )
    G.set_speaker("You", "right")
    G.print(
        "OMG! There are so many hate comments! "
        "I feel bad for him! JH doesn't deserve to receive all the hate because of this kind of fake news. "
    )

    while G.flags_dict.get("REACT_SNS") is None:
        reply = G.input(f"Should I defend JH? (y/n)?")
        reply = reply.lower()[:1]
        if reply == "y":
            G.flags_dict["REACT_SNS"] = True
        elif reply == "n":
            G.flags_dict["REACT_SNS"] = False

    # [Example]: Changing the chat messages based on flags set within scenario.
    if G.flags_dict["REACT_SNS"]:
        G.print("Yes! He deserves to be protected at all times.")
    else:
        G.print("Oh well, maybe next time.")


def event_dox(G: Controller):
    """DOX_HATER'S_FAMILY"""

    G.set_speaker("You", "Right")
    G.print(
        "How dare he say such a thing?"
        "Everyone has the right to live the life that they want to live! Even K-POP Idols!!"
        "Would you feel comfortable if your life got exposed like that? Being rumoured?"
        "I, the true fan of JH, will show you what it feels like to have your life exposed. "
        "You want to talk bad about my idol’s life? "
        "I will also show you how it feels to be talked bad."
    )

    G.set_speaker("ai", "left")
    G.print(
        "I started searching up all the things I could find about the hater. "
        "Digging all information i can find on Instagram, Facebook..."
        "Even information about their families. "
        "Where his brother is studying,"
        "Where his father is working,"
        "Where his mother enjoys to go for a walk…"
        "After spurring all the doxed information to him, "
        "He then blocked me and disappeared."
        "He must have been scared!"
        "Thats what it feels like…"
        "I won! I successfully defended my JH!!"
    )


# Yu Qing's
def event_reacttosns(G: Controller):
    """Reacting to hater"""
    G.set_speaker("You", "right")
    G.print("Why would you say such bad words about my idol?")

    G.set_speaker("Hater", "left")
    G.print(
        "He is just a trash-hole. He deserves all the hate that he is receiving right now. Go to hell"
    )
