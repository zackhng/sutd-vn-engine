import asyncio
from tkinter import *
from tkinter.ttk import *

# https://docs.python.org/3/library/tk.html
# https://docs.python.org/3/library/tkinter.ttk.html
FPS_60 = 0.015


def create_input_function(label: Label, inputbox: Text):
    """Emulates input function using GUI elements."""
    triggered = False

    def _trigger(*_, **__):
        nonlocal triggered
        triggered = True

    inputbox.bind("<Return>", _trigger)

    async def _input(text):
        nonlocal triggered
        label.configure(text=text)
        while not triggered:
            await asyncio.sleep(FPS_60)
        triggered = False
        prompt = inputbox.get("1.0", "end-2c")
        inputbox.delete("1.0", "end")
        return prompt

    return _input


def create_print_function(label: Label):
    def _print(text):
        label.configure(text=text)

    return _print


async def loop(app):
    """GUI Loop."""
    while True:
        app.update()
        await asyncio.sleep(FPS_60)


def create_gui(app):
    replybox = Label(app)
    textbox = Text(app)
    label = Label(app)
    replybox.pack()
    label.pack()
    textbox.pack()

    ginput = create_input_function(label, textbox)
    gprint = create_print_function(replybox)

    class _G:
        def __init__(self):
            self.input = ginput
            self.print = gprint

    return _G()


USER_PREFERENCE_IS_BURGER = None
USER_PREFERENCE_IS_GAY = False
FLAG_CAT_OR_DOG = False


async def scenario_food_tastes(G):
    global USER_PREFERENCE_IS_BURGER
    while USER_PREFERENCE_IS_BURGER is None:
        f = await G.input("Do you like sushi? 1 = Yes, 2 = No")
        if f == "1":
            USER_PREFERENCE_IS_BURGER = False
            G.print("I like sushi too!")
        elif f == "2":
            USER_PREFERENCE_IS_BURGER = True
            G.print("I like sushi more")
        else:
            G.print("I don't understand, Do you like sushi? 1 = Yes, 2 = No")


async def main():
    """Main entrypoint."""
    app = Tk()
    apptask = asyncio.create_task(loop(app))
    G = create_gui(app)

    await scenario_food_tastes(G)
    # await scenario_sex_preference(G)
    # await scenario_save_kitty(G)

    # await scenario_conclusion(G)
    await apptask


if __name__ == "__main__":
    asyncio.run(main())

"""
f = input (" Do you like hamburger? 1 = Yes, 2 = No ")
if f == 1 :
    print(" I like hamburger too")
else:
    print(" I like sushi more")

"""
