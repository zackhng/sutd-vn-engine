"""Underlying engine for VN game."""

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
from .image import Image
from .utils import ASSETS_DIR, EM, LOOP_WAIT, bind_toggle, set_canvas_bg, wait_coro
from .windowing import create_window

__all__ = ["Controller", "create_app", "run_story"]

log = logging.getLogger(__name__)


class Controller(NamedTuple):
    """Contains all key functions for controlling the GUI as one singleton."""

    root: tk.Tk
    """Root Tkinter widget."""
    flags_dict: Dict[str, Any]
    """Dictionary for storing arbitrary game flags."""
    input: Callable[[object], str]
    """Function to emulate `input()`."""
    print: Callable[..., None]
    """Function to emulate `print()`."""
    set_speaker: Callable
    """Function to set name & position of subsequent chat bubbles."""


def create_input_function(chatlog: ChatLog, inputbox: tk.Entry):
    """Emulates standard `input()` function using widgets.

    Input is triggered by pressing the Enter key inside `inputbox`.

    Args:
        chatlog (ChatLog): ChatLog widget to print to.
        inputbox (tk.Entry): Entry widget for input.

    Returns:
        Callable[[object], str]: Emulated `input()` function.
    """
    # Whether input is triggered.
    triggered = False

    def _trigger(_):
        """Callback to trigger input."""
        nonlocal triggered
        triggered = True

    async def _input(__prompt: object = "", /):
        """Emulates `input()`."""
        nonlocal triggered

        # Display prompt & enable input.
        text = str(__prompt)
        inputbox.config(state="normal")
        chatlog.add_msg(text, name="", side="center")
        logging.info(f"Wait prompt: {text}")

        # Block till input.
        while not triggered:
            await asyncio.sleep(LOOP_WAIT)
        triggered = False

        # Retrieve input.
        reply = inputbox.get()
        inputbox.delete("0", "end")
        inputbox.config(state="disabled")
        logging.info(f"Prompt: {text}, Return: {reply}")
        return reply

    # Disable input until `input()` is called.
    inputbox.config(state="disabled")
    inputbox.bind("<Return>", _trigger)
    logging.info("Input function binded.")
    return _input


def create_print_function(chatlog: ChatLog):
    """Emulates print function using GUI elements.

    By default, print is animated. To skip animation, `skipvar.set(True)`.

    Args:
        chatlog (ChatLog): ChatLog widget to print to.

    Returns:
        Tuple[Callable[..., None], tk.BooleanVar]: Emulated `print()` function,
            BooleanVar that can be set to skip animation.
    """
    skipvar = tk.BooleanVar(chatlog)

    async def _print(*values, sep=" "):
        """Emulates `print()`."""
        text = sep.join(map(str, values))
        logging.info(f"Print: {text}")

        # Whether animation is in progress.
        running = True

        async def _check_cancel():
            """Task that completes immediately when animation is skipped."""
            while running and not skipvar.get():
                await asyncio.sleep(LOOP_WAIT)

        async def _print_coro():
            """Animation task."""
            nonlocal running
            try:
                await chatlog.add_anim_msg(text)
            except tk.TclError:
                log.warning("App exited during print animation.")
            running = False

        task_cancel = asyncio.create_task(_check_cancel())
        task_print = asyncio.create_task(_print_coro())

        # To cancel anim early, race for `task_cancel` to complete first.
        await asyncio.wait(
            [task_cancel, task_print], return_when=asyncio.FIRST_COMPLETED
        )
        if running:
            task_print.cancel()
        await asyncio.gather(task_cancel, task_print)

    return _print, skipvar


def init_taskbar(root: tk.Misc):
    """Create taskbar layout in a `tk.Frame` as child of `root`."""
    taskbar = tk.Frame(root, bg="#245dda", relief="raised", bd=2)
    start_btn = tk.Button(
        taskbar,
        bg="#81c046",
        fg="white",
        text="Start",
        font=f"Verdana {EM[0]*1.4:.0f} italic",
    )
    start_btn.pack(side="left")

    return taskbar


def init_chat_win(canvas: tk.Canvas, loop: asyncio.AbstractEventLoop):
    """Create chat window inside `canvas`.

    The asyncio event `loop` is expected to be on the main thread due to Tkinter
    limitations. As such, the emulated `input()` and `print()` functions should
    be called from a separate "game thread" to prevent deadlock. `loop` is used
    to call `input()` and `print()`, which are coroutines, synchronously within
    the "game thread".

    Args:
        canvas (tk.Canvas): Canvas to create chat window in.
        loop (asyncio.AbstractEventLoop): Main thread event loop.

    Returns:
        Tuple[ChatLog, Callable[[object], str], Callable[..., None]]:
            ChatLog widget, emulated `input()` function, emulated `print()` function.
    """
    # Create widgets.
    bbox = (canvas.winfo_width() // 2 - 30 * EM[0], 5 * EM[0], 70 * EM[0], 70 * EM[0])
    chat_win = create_window(canvas, "Bubble", bbox)
    chatlog = ChatLog(chat_win)
    textbox = ttk.Entry(chat_win)
    skipbtn = tk.Button(chat_win, text="Skip")

    # Configure grid layout.
    chat_win.rowconfigure(11, minsize=EM[0])
    chat_win.rowconfigure([*range(11)], weight=1)
    chat_win.columnconfigure([*range(12)], weight=1)

    # Place widgets.
    chatlog.grid(sticky="nsew", row=0, columnspan=12, rowspan=11)
    skipbtn.grid(sticky="nsew", row=11, column=0, columnspan=2)
    textbox.grid(sticky="nsew", row=11, column=2, columnspan=10)

    # Create emulated `input()` and `print()` functions.
    _input = create_input_function(chatlog, textbox)
    _print, skipvar = create_print_function(chatlog)

    def _ginput(*args, **kwargs):
        """Synchronous wrapper for `input()`."""
        return wait_coro(_input(*args, **kwargs), loop)

    def _gprint(*args, **kwargs):
        """Synchronous wrapper for `print()`."""
        return wait_coro(_print(*args, **kwargs), loop)

    bind_toggle(skipbtn, skipvar, "Skipping", "Skip")
    return chatlog, _ginput, _gprint


def init_gui(loop: asyncio.AbstractEventLoop):
    """Creates GUI and `Controller` singleton.

    Asyncio event `loop` is required for `init_chat_win()`. See `init_chat_win()`
    for more details.
    """
    root = tk.Tk()
    root.title("SUTD VN")
    root.attributes("-fullscreen", True)
    root.update_idletasks()

    # NOTE: Dirty hack to change global scale.
    # root.tk.call("tk", "scaling", 2.0) # Doesn't work.
    screen_h = root.winfo_screenheight()
    if screen_h >= 2160:
        EM[0] = 20
    elif screen_h >= 1440:
        EM[0] = 10
    elif screen_h >= 1080:
        EM[0] = 8
    else:
        EM[0] = 8

    # Configure global font.
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.config(family="Courier New", size=EM[0])
    root.option_add("*Font", default_font)

    # Canvas that serves as "desktop".
    canvas = tk.Canvas(root, bg="#e28de2")
    set_canvas_bg(canvas, f"{ASSETS_DIR}/windoes_background.png")

    taskbar = init_taskbar(root)

    canvas.pack(fill="both", side="top", expand=True)
    taskbar.pack(fill="x", side="bottom")

    # Run one update loop to update widget sizes for subsequent relative widget
    # placements to work.
    root.update()

    chatlog, _ginput, _gprint = init_chat_win(canvas, loop)
    webcam_bbox = (0, 0, 60 * EM[0], 60 * EM[0])
    webcam = create_window(canvas, "Face Cam", webcam_bbox, disable_resize=True)
    face_img = Image(webcam, img_fp=f"{ASSETS_DIR}/sutd.png")
    face_img.pack(fill="both", expand=True)

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
    """Init & run app, then clean up when exiting."""
    _G = init_gui(asyncio.get_running_loop())

    # Whether app should continue running.
    running = True

    async def _loop():
        """Tkinter GUI update loop task."""
        logging.info("GUI loop started.")
        while running:
            _G.root.update()
            await asyncio.sleep(LOOP_WAIT)
        logging.info("GUI loop stopped.")

        # Clean up all asyncio tasks on exit.
        for task in asyncio.all_tasks():
            task.cancel()

    def _on_quit():
        """Callback for when app is closed."""
        nonlocal running
        running = False
        _G.root.destroy()
        _G.root.quit()
        logging.info("App quitting...")

    asyncio.create_task(_loop())
    _G.root.protocol("WM_DELETE_WINDOW", _on_quit)

    try:
        yield _G
    finally:
        if running:
            _on_quit()


def run_story(story: Callable[[Controller], Any]):
    """Run `story` function in separate "game thread"."""
    logging.basicConfig(level=logging.INFO)

    def _wrapper(G: Controller):
        """Wrapper to ensure errors are reported."""
        try:
            story(G)
        except futures.CancelledError:
            pass
        except Exception as e:
            log.exception("Error while executing story", exc_info=e)
            raise e

    async def _run_story():
        """Asyncio entrypoint task."""
        try:
            async with create_app() as G:
                # Run story in separate "game thread".
                await asyncio.to_thread(_wrapper, G)

                # Don't exit when "game thread" finishes.
                while True:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    try:
        asyncio.run(_run_story())
    except KeyboardInterrupt:
        pass
