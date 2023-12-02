"""Hyun's build up scenarios."""

from sutd_vn_engine.engine import Controller

__all__ = ["event_social_media", "event_dox"]


def event_social_media(G: Controller):
    """Social Media Event"""
    if G.flags_dict.get("GAMEOVER"):
        return
    G.set_speaker("", "center")
    G.print("1 month later")
    G.set_speaker("Narrator", "left")
    """Changing facial expression to fit the sanity level of Character"""
    G.show_face("face_interested")
    G.print(
        "Now you are a electric fan of JH. You have been following his social media "
        "accounts and have been keeping up with his latest news. "
    )
    G.print(
        "As you were mopping vomit from the floor, a notification popped up on your phone. "
    )

    # Set who is speaking, and on what side the chat bubble appears.
    # i.e., "left", "right", or "center".
    G.set_speaker("News", "left")
    G.print(
        "*BREAKING* JH HAS BEEN DATING?!?!! "
        "JH has been reportedly dating a fan for several years. "
        "Since last year, many of JH fans had suspected as such, "
        "posting on forums and fan sites images of ‘JH Dating Ordinary Person’ evidence. "
        "The ‘evidence’ includes pictures of the two of them together, "
        "looking at each other lovingly, the two with couple items..."
    )
    # Split very long text across multiple lines.
    G.set_speaker("You", "right")
    """Changing facial expression to fit the sanity level of Character"""
    G.show_face("face_obsessed1")
    G.print(
        "Hm? whats this? (⚆_⚆) "
        "JH is dating?? Thats ridiculous. "
        "He is loyal to his fans and to his fans only. "
        "No one should believe this kind of stupid rumours. "
        "I like my Idol JH and thus I trust him. I should maintain my stance as a fan."
    )
    G.print(
        "JH is going have his world tour soon... "
        "I hope this rumour doesn't ruin his feelings before his performance. "
        "I should look into the comments if there is any comments that may possibly hurt him. "
    )
    G.set_speaker("Haters", "left")
    G.print(
        "Ew.. what kind of idol is he? "
        "Can't believe he betrayed all his fans... "
        "Very disappointing. Quit Your job as an Idol. ୧༼ಠ益ಠ༽୨ "
    )
    G.set_speaker("You", "right")
    G.print(
        "OMG! There are so many hate comments! (#｀皿´) "
        "I feel bad for him! JH doesn't deserve to receive all the hate because of this kind of fake news. "
    )

    while G.flags_dict.get("REACT_SNS") is None:
        reply = G.input(f"Should I defend JH? (y/n)?")
        reply = reply.lower()[:1]
        if reply == "y":
            """Returning REACT_SNS True/False to trigger or skip future events"""
            G.flags_dict["REACT_SNS"] = True
        elif reply == "n":
            G.flags_dict["REACT_SNS"] = False

    # [Example]: Changing the chat messages based on flags set within scenario.
    if G.flags_dict["REACT_SNS"]:
        G.print("Yes! He deserves to be protected at all times. ╰༼=ಠਊಠ=༽╯ ")
    else:
        """Changing facial expressions to fit the insanity level of character"""
        G.show_face("face_interested")
        G.print("Oh well... I have better things to do.")

        G.set_speaker("Narrator", "left")
        G.print(
            "Anyways, you went back to work. Which you did decently at for the next "
            "few weeks."
        )


def event_dox(G: Controller):
    """DOX_HATER'S_FAMILY."""
    """Skip event if flags return True for GAMEOVER or REACT_SNS return False"""
    if G.flags_dict.get("GAMEOVER") or not G.flags_dict.get("REACT_SNS"):
        return

    G.set_speaker("You", "right")
    """Changing facial expression to fit the insanity level of Character"""
    G.show_face("face_obsessed2")
    G.print(
        "How dare he say such a thing? "
        "Everyone has the right to live the life that they want to live! Even K-POP Idols!! ಥ_ಥ "
        "Would you feel comfortable if your life got exposed like that? Being rumoured? "
        "I, the true fan of JH, will show you what it feels like to have your life exposed. "
        "You want to talk bad about my idol's life? "
        "I will also show you how it feels to be talked bad. ಥ_ಥ "
    )

    G.set_speaker("", "right")
    G.print(
        "I started searching up all the things I could find about the hater. ⨀_⨀ "
        "Digging all information i can find on Instagram, Facebook... "
        "Even information about their families. "
        "Where his brother is studying, "
        "Where his father is working, "
        "Where his mother enjoys to go for a walk... ヽ༼ ಠ益ಠ ༽ﾉ"
        "After spurring all the doxed information to him, "
        "He then blocked me and disappeared. "
        "He must have been scared! "
        "Thats what it feels like... (◔ᴥ◔) "
        "I won! I successfully defended my JH!!! (⌣̀_⌣́)"
    )

    G.set_speaker("Narrator", "left")
    G.print(
        "With that, you fell further down the rabbit hole of the internet and "
        "became a full-fledged obsessive fan. Your boss has also become quite "
        "concerned about your performance at work. But you didn't care. "
    )
