"""Utilities and constants."""

import asyncio
import tkinter as tk
from typing import Coroutine

__all__ = ["LOOP_WAIT", "EM", "LORUM", "wait_coro", "bind_toggle"]

LOOP_WAIT = 0.015
"""60Hz loop sleep. Sleep is needed in asyncio to process other events."""
EM = 10  # In px.
"""Global size used for fonts, padding, and so on."""
LORUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at "
    "elit non orci luctus porta et sit amet turpis. Vestibulum magna velit, "
    "finibus vel luctus vitae, condimentum eleifend diam. Maecenas ultrices "
    "neque at orci porta, a gravida eros aliquam. Phasellus eget ex placerat, "
    "condimentum nunc eget, convallis ante. Quisque feugiat magna massa, sit "
    "amet consectetur velit iaculis non. Aliquam nec."
)


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
