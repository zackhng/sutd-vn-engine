from sutd_vn_engine.engine import Controller

__all__ = ["event_ending"]


def ending_kys(G: Controller):
    G.set_speaker("You", "right")
    G.show_face("background")
    G.print(
        "It seems that my life is now meaningless now that my idol has found a partner. "
    )
    G.print(
        "I feel lost and betrayed. How can he do this to us? I have been supporting him since day 1 and this is how he treat us fans? "
    )
    G.print(
        "I actually believed I stood a chance to get together with him. Now that he has a girlfriend, it seems like I have lost my purpose in life. I don’t know what to do now. "
    )
    G.print("I think it is time for me to end my life.")
    G.show_jumpscare()


def ending_therapy(G: Controller):
    G.set_speaker("You", "right")
    G.show_face("background")
    G.print(
        "I couldn't stop myself this time from actually breaking into their dorm, but knowing that it is wrong to break in. "
    )
    G.print(
        "I was curious… All I wanted to know was what they were doing in the hotel, what food they were eating, their lifestyle, and everything! "
    )
    G.print("My urge to break in a lot stronger than my moral sense. ")
    G.print("I was caught because I wasn't careful enough. This is all my fault... ")


def ending_true_fan(G: Controller):
    G.set_speaker("Narrator", "left")
    G.print(
        "Congratulations, you are a true fan! You chose to maintain a healthy and balanced relationship with your idols and your personal connections. "
        "Keep in mind that parasocialism can be positive, but only in moderation. "
        "Always take a reality check and never forsake your well being for strangers. "
        "May your journey be filled with genuine connections and thank you for making the right choices in a world that is ever-increasingly dominated by digital illusions. "
    )


def ending_mid(G: Controller):
    G.set_speaker("You", "right")
    G.print(
        "I could stop myself this time from actually breaking into their dorm, but i did feel the urge to break in and see their rooms and get their items! "
    )
    G.print(
        "I am curious… I want to know how they are living in their dorms, what food they are eating, their lifestyle, and everything! "
    )
    G.print(
        "I just stopped myself because it is illegal and my moral sense is still stronger than my urge to break in. "
    )
    G.print(
        "But what if the urge becomes stronger? the desire to know more about them gets bigger than my moral sense? "
    )
    G.print("Will I be able to stop myself then? ")
    G.print("I don't know what to do…")


def ending_boring(G: Controller):
    G.set_speaker("Narrator", "left")
    G.print(
        "You have reached the ending. It seems that you are someone that is digitally responsible. It is melancholy but you're not really into idols anymore. "
        "Sure, you listen to the music from time to time but you seem to have better things to do than to stalk idols on the internet. "
        "I commend you for being digitally responsible in a world where internet addiction has become an increasingly concerning problem."
    )


def event_ending(G: Controller):
    """Check which ending is triggered."""
    G.set_speaker("", "center")
    G.print("You have Reach the End")
    G.print("In conclusion...")
    if not G.flags_dict.get("ACCEPT_JOB"):
        ending_boring(G)
    elif G.flags_dict.get("BREAK_INTO_HOTEL"):
        if G.flags_dict.get("GAME_WIN"):
            ending_kys(G)
        else:
            ending_therapy(G)
    else:
        if G.flags_dict.get("PERSUADE_FRIEND"):
            ending_true_fan(G)
        else:
            ending_mid(G)
