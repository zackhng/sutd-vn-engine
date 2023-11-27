"""Main app."""

##################
# YOUR CODE HERE #
##################
# Import anything you need, like math.

from sutd_vn_engine.engine import Controller, run_story


def event_example(G: Controller):
    """Example event."""
    # Set who is speaking, and on what side the chat bubble appears.
    # i.e., "left", "right", or "center".
    G.set_speaker("You", "right")

    # Print something out just like `print()`.
    G.print("Hello world.")
    # Split very long text across multiple lines.
    G.print(
        "lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum"
        " at elit non orci luctus porta et sit amet turpis. Vestibulum magna"
    )
    # Get user input just like `input()`.
    name = G.input("What is your name?")
    G.flags_dict["USERNAME"] = name

    # Switch what news article is shown.
    # G.show_news("job_offer.png")

    # Switch what face expression is shown.
    # G.show_face("sparkling_eyes.png")

    # [Example] Waiting for valid user input to set flag & proceed.
    while G.flags_dict.get("ACCEPTED_JOB") is None:
        reply = G.input(f"So {G.flags_dict['USERNAME']}, do you accept the job (y/n)?")
        reply = reply.lower()
        if reply[0] == "y":
            G.flags_dict["ACCEPTED_JOB"] = True
        elif reply[0] == "n":
            G.flags_dict["ACCEPTED_JOB"] = False

    # [Example]: Changing the chat messages based on flags set within scenario.
    if G.flags_dict["ACCEPTED_JOB"]:
        G.print("Great! See you at the office tomorrow.")
    else:
        G.print("Oh well, maybe next time.")

    # [Example]: Changing the chat messages based on flags from previous scenarios.
    if G.flags_dict.get("ACCEPTED_PET_CAT"):
        G.print("You also got a cat!")


# Duplicate the below function as many times as needed for each scenario you are writing.
def event_your_event(G: Controller):
    """Event."""
    ##################
    # YOUR CODE HERE #
    ##################


def story(G: Controller):
    """Storyline."""
    ##################
    # YOUR CODE HERE #
    ##################
    # Test any flags your scenario relies on by setting them here beforehand.
    G.flags_dict["ACCEPTED_PET_CAT"] = True
    event_your_event(G)

    # Comment out below example once satisfied.
    event_example(G)


if __name__ == "__main__":
    run_story(story)
