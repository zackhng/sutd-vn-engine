"""Utility for creating windowed frames."""

import tkinter as tk

from .utils import EM

__all__ = ["create_window"]


def create_window(canvas, title, bbox):
    """Create a windowed frame.

    Note that w & h specifies the internal frame size, excluding the window bar.
    """
    x, y, w, h = bbox
    bar_h = 4 * EM

    win = tk.Frame(canvas, bd=0, width=w, height=h + bar_h)
    content = tk.Frame(win, bd=2, relief="ridge")
    bar = tk.Frame(win, bd=2, bg="lightblue", relief="raised")
    title = tk.Label(bar, text=title, font=f"Verdana {EM}", bg="lightblue")

    bar.place(x=0, y=0, width=w, height=bar_h)
    content.place(x=0, y=bar_h, width=w, height=h)
    title.pack(side="left")

    win_id = canvas.create_window((x, y), window=win, anchor="n")

    def _move_win(_):
        x0, y0 = canvas.winfo_pointerxy()
        x0 -= canvas.winfo_rootx()
        y0 -= canvas.winfo_rooty()
        canvas.coords(win_id, x0, y0)

    shaded = False

    def _shade_win(_):
        nonlocal shaded
        if shaded:
            canvas.itemconfigure(win_id, state="normal")
        else:
            canvas.itemconfigure(win_id, state="hidden")
        shaded = not shaded

    bar.bind("<B1-Motion>", _move_win)
    title.bind("<B1-Motion>", _move_win)
    # bar.bind("<Button-1>", _shade_win)
    # title.bind("<Button-1>", _shade_win)

    return content
