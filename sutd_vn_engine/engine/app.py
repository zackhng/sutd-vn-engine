"""Underlying engine for VN."""

import asyncio
import logging

# https://docs.python.org/3/library/tk.html
# https://docs.python.org/3/library/tkinter.ttk.html
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from concurrent import futures
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict, NamedTuple

from .chat import ChatLog
from .utils import EM, LOOP_WAIT, make_toggle, wait_coro
from .windowing import create_window

__all__ = ["Controller", "create_app", "run_story"]

log = logging.getLogger(__name__)


class Controller(NamedTuple):
    """GUI controller."""

    root: tk.Tk
    flags_dict: Dict[str, Any]
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


def init_taskbar(root):
    """Create taskbar."""
    taskbar = tk.Frame(root, background="lightgray", relief="raised", bd=2)
    start_btn = tk.Button(taskbar, text="⊞", font="Arial 20")
    start_btn.pack(side="left")

    return taskbar


def init_chat_win(canvas, loop):
    """Create chat window."""
    chat_win = create_window(
        canvas,
        "WhatsUp",
        (canvas.winfo_width(), canvas.winfo_height(), 20 * EM, 20 * EM),
    )
    chatlog = ChatLog(chat_win)
    textbox = ttk.Entry(chat_win)
    skipbtn = tk.Button(chat_win, text="Skip")

    chatlog.grid(sticky="nsew", row=0, columnspan=12, rowspan=11)
    skipbtn.grid(sticky="ew", row=11, column=0, columnspan=2)
    textbox.grid(sticky="nsew", row=11, column=2, columnspan=10)

    _input = create_input_function(chatlog, textbox)
    _print, skipvar = create_print_function(chatlog)
    make_toggle(skipbtn, skipvar, "Skipping", "Skip")

    def _ginput(*args, **kwargs):
        return wait_coro(_input(*args, **kwargs), loop)

    def _gprint(*args, **kwargs):
        return wait_coro(_print(*args, **kwargs), loop)

    return chatlog, _ginput, _gprint


def init_gui(loop):
    """Init GUI and GUI controller."""
    root = tk.Tk()
    root.title("SUTD VN")

    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.config(family="Courier New", size=EM)
    root.option_add("*Font", default_font)

    canvas = tk.Canvas(root, background="pink")
    taskbar = init_taskbar(root)

    canvas.pack(fill="both", side="top", expand=True)
    taskbar.pack(fill="x", side="bottom")
    root.update()

    chatlog, _ginput, _gprint = init_chat_win(canvas, loop)

    _G = Controller(
        root=root,
        flags_dict={},
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

        # Clean up asyncio tasks.
        for task in asyncio.all_tasks():
            task.cancel()

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

    def _wrapper(*args, **kwargs):
        try:
            story(*args, **kwargs)
        except futures.CancelledError:
            pass
        except Exception as e:
            log.exception("Error while executing story", exc_info=e)
            raise e

    async def _run_story():
        try:
            async with create_app() as G:
                await asyncio.to_thread(_wrapper, G)
                while True:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    try:
        asyncio.run(_run_story())
    except KeyboardInterrupt:
        pass
