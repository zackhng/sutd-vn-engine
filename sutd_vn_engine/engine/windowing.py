"""Utility for creating windowed frames."""

import tkinter as tk

from .utils import EM

__all__ = ["create_window"]


def create_window(canvas, title, bbox, u=12):
    """Create a windowed frame."""
    x, y, w, h = bbox
    bar_h = 2 * EM

    win = tk.Frame(canvas, relief="ridge", bd=2)
    bar = tk.Frame(win, bg="lightblue", relief="raised", bd=2)
    content = tk.Frame(win)
    title = tk.Label(bar, text=title, font=f"Verdana {EM}", bg="lightblue")

    win.grid_rowconfigure(0, minsize=bar_h, weight=1)
    win.grid_rowconfigure(1, minsize=h - bar_h, weight=1)
    content.grid_rowconfigure(list(range(u)), minsize=(h - bar_h) / u, weight=1)
    content.grid_columnconfigure(list(range(u)), minsize=w / u, weight=1)

    bar.grid(sticky="nsew", row=0)
    content.grid(sticky="nsew", row=1)
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
