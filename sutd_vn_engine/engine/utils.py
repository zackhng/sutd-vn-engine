"""Utilities and constants."""

import asyncio
import tkinter as tk
from pathlib import Path
from typing import Coroutine

import sutd_vn_engine.assets

__all__ = [
    "LOOP_WAIT",
    "EM",
    "LORUM",
    "ASSETS_DIR",
    "wait_coro",
    "bind_toggle",
    "add_bind_tag",
    "set_canvas_bg",
]

LOOP_WAIT = 0.008
"""60Hz loop sleep. Sleep is needed in asyncio to process other events."""
# NOTE: Put in a list to be mutable.
EM = [2]  # In px.
"""Global size used for fonts, padding, and so on."""
LORUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at "
    "elit non orci luctus porta et sit amet turpis. Vestibulum magna velit, "
    "finibus vel luctus vitae, condimentum eleifend diam. Maecenas ultrices "
    "neque at orci porta, a gravida eros aliquam. Phasellus eget ex placerat, "
    "condimentum nunc eget, convallis ante. Quisque feugiat magna massa, sit "
    "amet consectetur velit iaculis non. Aliquam nec."
)
ASSETS_DIR = Path(sutd_vn_engine.assets.__path__[0]).absolute()
"""Path to `sutd_vn_engine/assets` folder."""


def wait_coro(coro: Coroutine, loop: asyncio.AbstractEventLoop):
    """Schedule coroutine to run in event loop and wait for it to finish.

    Must be called from a different thread than the event loop or it will deadlock.

    Args:
        coro (Coroutine): Coroutine to wait for.
        loop (asyncio.AbstractEventLoop, optional): Asyncio event loop to use.

    Returns:
        Any: Return value of the coroutine.
    """
    try:
        cur_loop = asyncio.get_running_loop()
    except RuntimeError:
        cur_loop = None

    if cur_loop is loop:
        raise RuntimeError(
            "Calling `wait_coro()` on same thread as `loop` will deadlock."
        )

    future = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        return future.result()
    finally:
        future.cancel()


def bind_toggle(button: tk.Button, boolvar: tk.BooleanVar, onlabel: str, offlabel: str):
    """Bind `button` to `boolvar` as a toggle.

    Args:
        button (tk.Button): Button to bind.
        boolvar (tk.BooleanVar): Boolean variable to bind to.
        onlabel (str): Text to display when `boolvar` is True.
        offlabel (str): Text to display when `boolvar` is False.
    """

    def _update():
        """Update button text & style."""
        if boolvar.get():
            button.config(text=onlabel, fg="green")
        else:
            button.config(text=offlabel, fg="red")

    def _toggle():
        """Toggle `boolvar` and update button."""
        boolvar.set(not boolvar.get())
        _update()

    button.config(command=_toggle)
    _update()

    # Update icon when boolvar is changed.
    boolvar.trace_add("write", lambda *_: _update())


def add_bind_tag(tag: str, *widgets: tk.Widget):
    """Add bind tag to each widget.

    Args:
        tag (str): Tag to add.
        *widgets (tk.Widget): Widgets to add tag to.
    """
    for widget in widgets:
        widget.bindtags((tag,) + widget.bindtags())


def set_canvas_bg(canvas: tk.Canvas, image_path: str):
    """Set background image of `canvas` to `image_path`."""
    img = tk.PhotoImage(master=canvas, file=image_path)
    img_id = canvas.create_image(0, 0, image=img, anchor="center")

    def _recale_bg(event: tk.Event):
        """Re-scale background image to fit canvas."""
        # NOTE: Tkinter only supports integer zooming, this hurts me.
        if event.width > img.width():
            new_img = img.zoom(max(round(event.width / img.width()), 1))
        else:
            new_img = img.subsample(max(round(img.width() / event.width), 1))

        # Set new background & center it.
        canvas.itemconfig(img_id, image=new_img)
        canvas.coords(img_id, event.width // 2, event.height // 2)
        setattr(canvas, "bg_img", new_img)  # Prevent GC.

    canvas.bind("<Configure>", _recale_bg, "+")
