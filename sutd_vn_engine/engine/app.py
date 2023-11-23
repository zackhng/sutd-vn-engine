"""Underlying engine for VN."""

import asyncio
import logging

# https://docs.python.org/3/library/tk.html
# https://docs.python.org/3/library/tkinter.ttk.html
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from contextlib import asynccontextmanager
from typing import Callable, Dict, NamedTuple

from sutd_vn_engine.engine.chat import ChatLog
from sutd_vn_engine.engine.utils import EM, LOOP_WAIT, make_toggle, wait_coro

__all__ = ["Controller", "create_app", "run_story"]

log = logging.getLogger(__name__)


class Controller(NamedTuple):
    """GUI controller."""

    root: tk.Tk
    flags: Dict[str, bool]
    input: Callable[[object], str]
    print: Callable[..., None]
    set_speaker: Callable


def create_input_function(chatlog: ChatLog, inputbox: ttk.Entry):
    """Emulates input function using GUI elements."""
    triggered = False

    def _trigger(*_):
        nonlocal triggered
        triggered = True

    async def _input(__prompt: object = "", /):
        nonlocal triggered
        text = str(__prompt)
        logging.info(f"Wait prompt: {text}")
        inputbox.config(state=tk.NORMAL)
        chatlog.add_msg(text, name="", side=tk.CENTER)
        while not triggered:
            await asyncio.sleep(LOOP_WAIT)
        triggered = False
        reply = inputbox.get()
        inputbox.delete("0", "end")
        inputbox.config(state=tk.DISABLED)
        logging.info(f"Prompt: {text}, Return: {reply}")
        return reply

    inputbox.bind("<Return>", _trigger)
    inputbox.config(state=tk.DISABLED)
    logging.info("Input function binded.")
    return _input


def create_print_function(chatlog: ChatLog):
    """Emulates print function using GUI elements."""
    skipvar = tk.BooleanVar()

    async def _print(*values, sep=" "):
        text = sep.join(map(str, values))
        logging.info(f"Print: {text}")

        running = True

        async def _check_cancel():
            nonlocal running
            while running and not skipvar.get():
                await asyncio.sleep(LOOP_WAIT)

        async def _print_coro():
            nonlocal running
            await chatlog.add_anim_msg(text)
            running = False

        task_cancel = asyncio.create_task(_check_cancel())
        task_print = asyncio.create_task(_print_coro())

        await asyncio.wait(
            [task_cancel, task_print], return_when=asyncio.FIRST_COMPLETED
        )
        if running:
            task_print.cancel()
        await asyncio.gather(task_cancel, task_print)

    return _print, skipvar


def init_gui(loop):
    """Init GUI and GUI controller."""
    root = tk.Tk()
    root.title("SUTD VN")

    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.config(family="Courier New", size=EM)
    root.option_add("*Font", default_font)

    canvas = tk.Canvas(root, background="pink")
    taskbar = tk.Frame(root, background="lightgray", relief="raised", bd=4)
    start_btn = tk.Button(taskbar, text="⊞", font="Arial 20")
    chat_win = ttk.Frame(canvas)
    chatlog = ChatLog(chat_win)
    textbox = ttk.Entry(chat_win)
    skipbtn = tk.Button(chat_win, text="Skip")

    chatlog.grid(sticky="nsew", row=0, column=0, columnspan=12)
    skipbtn.grid(sticky="ew", row=1, column=0, columnspan=2)
    textbox.grid(sticky="ew", row=1, column=2, columnspan=10)
    canvas.pack(fill="both", side="top", expand=True)
    taskbar.pack(fill="x", side="bottom")
    start_btn.pack(side="left")

    root.update()
    canvas.create_window(
        (canvas.winfo_width(), canvas.winfo_height()), window=chat_win, anchor="center"
    )

    _input = create_input_function(chatlog, textbox)
    _print, skipvar = create_print_function(chatlog)
    make_toggle(skipbtn, skipvar, "Skipping", "Skip")

    def _ginput(*args, **kwargs):
        return wait_coro(_input(*args, **kwargs), loop)

    def _gprint(*args, **kwargs):
        return wait_coro(_print(*args, **kwargs), loop)

    _G = Controller(
        root=root,
        flags={},
        input=_ginput,
        print=_gprint,
        set_speaker=chatlog.set_speaker,
    )
    logging.info("GUI initialized.")
    return _G


@asynccontextmanager
async def create_app():
    """Init app and run."""
    _G = init_gui(asyncio.get_running_loop())
    running = True

    async def _loop():
        logging.info("GUI loop started.")
        while running:
            _G.root.update()
            await asyncio.sleep(LOOP_WAIT)
        logging.info("GUI loop stopped.")
        raise KeyboardInterrupt

    asyncio.create_task(_loop())

    def _on_quit():
        nonlocal running
        running = False
        _G.root.destroy()
        _G.root.quit()
        logging.info("App ended.")

    _G.root.protocol("WM_DELETE_WINDOW", _on_quit)

    try:
        yield _G
    finally:
        if running:
            _on_quit()


def run_story(story):
    """Run story."""
    logging.basicConfig(level=logging.INFO)

    async def _run_story():
        async with create_app() as G:
            await asyncio.to_thread(story, G)
            while True:
                await asyncio.sleep(1)

    try:
        asyncio.run(_run_story())
    except KeyboardInterrupt:
        pass
