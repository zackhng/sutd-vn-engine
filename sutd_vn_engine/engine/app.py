"""Underlying engine for VN."""

import asyncio
import logging
from contextlib import asynccontextmanager
from tkinter import *
from tkinter.ttk import *  # type: ignore
from typing import Awaitable, Callable, Dict, NamedTuple

# https://docs.python.org/3/library/tk.html
# https://docs.python.org/3/library/tkinter.ttk.html

__all__ = ["Controller", "create_app"]

log = logging.getLogger(__name__)

LOOP_WAIT = 0.015


class Controller(NamedTuple):
    """GUI controller."""

    tk: Tk
    flags: Dict[str, bool]
    input: Callable[[object], Awaitable[str]]
    print: Callable[..., None]


def create_input_function(label: Label, inputbox: Entry):
    """Emulates input function using GUI elements."""
    triggered = False

    def _trigger(*_):
        nonlocal triggered
        triggered = True

    async def _input(__prompt: object = "", /):
        nonlocal triggered
        text = str(__prompt)
        logging.info(f"Wait prompt: {text}")
        inputbox.configure(state="normal")
        label.configure(text=text)
        while not triggered:
            await asyncio.sleep(LOOP_WAIT)
        triggered = False
        reply = inputbox.get()
        inputbox.delete("0", "end")
        inputbox.configure(state="disabled")
        logging.info(f"Prompt: {text}, Return: {reply}")
        return reply

    inputbox.bind("<Return>", _trigger)
    inputbox.configure(state="disabled")
    logging.info("Input function binded.")
    return _input


def create_print_function(label: Label):
    """Emulates print function using GUI elements."""

    def _print(*values, sep=" "):
        text = sep.join(map(str, values))
        logging.info(f"Print: {text}")
        label.configure(text=text)

    return _print


def init_gui():
    """Init GUI and GUI controller."""
    tk = Tk()
    replybox = Label(tk)
    textbox = Entry(tk)
    label = Label(tk)
    replybox.pack()
    label.pack()
    textbox.pack()

    _G = Controller(
        tk=tk,
        flags={},
        input=create_input_function(label, textbox),
        print=create_print_function(replybox),
    )
    logging.info("GUI initialized.")
    return _G


@asynccontextmanager
async def create_app():
    """Init app and run."""
    _G = init_gui()
    running = True

    async def _loop():
        nonlocal running
        logging.info("GUI loop started.")
        while running:
            _G.tk.update()
            await asyncio.sleep(LOOP_WAIT)
        logging.info("GUI loop stopped.")
        raise KeyboardInterrupt

    loop_task = asyncio.create_task(_loop())

    def _on_quit():
        nonlocal running, loop_task
        running = False
        _G.tk.destroy()
        _G.tk.quit()
        logging.info("App ended.")

    _G.tk.protocol("WM_DELETE_WINDOW", _on_quit)

    try:
        yield _G
    finally:
        if running:
            _on_quit()
