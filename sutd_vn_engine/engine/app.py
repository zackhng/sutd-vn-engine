"""Underlying engine for VN."""

import asyncio
import logging
from contextlib import asynccontextmanager

# https://docs.python.org/3/library/tk.html
# https://docs.python.org/3/library/tkinter.ttk.html
from tkinter import *
from tkinter.ttk import *  # type: ignore
from typing import Callable, Dict, NamedTuple

from sutd_vn_engine.engine.chat import ChatLog
from sutd_vn_engine.engine.utils import LOOP_WAIT, wait_coro

__all__ = ["Controller", "create_app"]

log = logging.getLogger(__name__)


class Controller(NamedTuple):
    """GUI controller."""

    root: Tk
    flags: Dict[str, bool]
    input: Callable[[object], str]
    print: Callable[..., None]
    set_speaker: Callable


def create_input_function(chatlog: ChatLog, inputbox: Entry):
    """Emulates input function using GUI elements."""
    triggered = False

    def _trigger(*_):
        nonlocal triggered
        triggered = True

    async def _input(__prompt: object = "", /):
        nonlocal triggered
        text = str(__prompt)
        logging.info(f"Wait prompt: {text}")
        inputbox.config(state=NORMAL)
        chatlog.add_message(text, name="", side=CENTER)
        while not triggered:
            await asyncio.sleep(LOOP_WAIT)
        triggered = False
        reply = inputbox.get()
        inputbox.delete("0", "end")
        inputbox.config(state=DISABLED)
        logging.info(f"Prompt: {text}, Return: {reply}")
        return reply

    inputbox.bind("<Return>", _trigger)
    inputbox.config(state=DISABLED)
    logging.info("Input function binded.")
    return _input


def create_print_function(chatlog: ChatLog):
    """Emulates print function using GUI elements."""

    async def _print(*values, sep=" "):
        text = sep.join(map(str, values))
        logging.info(f"Print: {text}")
        chatlog.add_message(text)

    return _print


def init_gui(loop):
    """Init GUI and GUI controller."""
    root = Tk()
    root.title("SUTD VN")
    root.configure(bg="pink")
    root.geometry("1280x960")
    root.resizable(width=False, height=False)

    chatlog = ChatLog(root)
    textbox = Entry(root)
    chatlog.pack(fill=Y, expand=True)
    textbox.pack()

    _input = create_input_function(chatlog, textbox)
    _print = create_print_function(chatlog)

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

    loop_task = asyncio.create_task(_loop())

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
