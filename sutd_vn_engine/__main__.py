"""Main app."""
import asyncio
import logging

from sutd_vn_engine.engine import Controller, create_app

USER_PREFERENCE_IS_BURGER = None
USER_PREFERENCE_IS_GAY = False
FLAG_CAT_OR_DOG = False


def calculate_beginning_score(flags):
    score = 0
    if flags.get("LIKES_BURGER"):
        score += 1

    return score


async def event_security_job(G: Controller):
    G.print(
        """
Inner Monologue:
Oh a nice job offer. Would it be nice?
"""
    )
    # G.show_news("job_offer.png")
    # G.show_face("sparkling_eyes.png")
    score = calculate_beginning_score(G.flags)
    if score > 10:
        G.print("We are in boys, time to stalk.")
    elif score > 3:
        G.print("Oh I might get to see my idol!")
    else:
        G.print("Nice opportunity to make money!")
    if score > 3 and G.flags.get("BOUGHT_MERCH"):
        G.print("maybe my idol can sign it!")
    while G.flags.get("ACCEPTED_JOB") is None:
        reply = await G.input("Do you accept the job (y/n)?")
        reply = reply.lower()
        if reply[0] == "y":
            G.flags["ACCEPTED_JOB"] = True
        elif reply[0] == "n":
            G.flags["ACCEPTED_JOB"] = False


async def main():
    """Main entrypoint."""
    async with create_app() as G:
        await event_security_job(G)
        # await scenario_sex_preference(G)
        # await scenario_save_kitty(G)
        # await scenario_conclusion(G)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
