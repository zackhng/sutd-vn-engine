"""Utility for creating windowed frames in a canvas."""

import tkinter as tk
from typing import Tuple

from .utils import EM

__all__ = ["create_window"]


def create_window(canvas: tk.Canvas, title: str, bbox: Tuple[int, int, int, int]):
    """Create a windowed frame.

    Note that w & h specifies the internal frame size, excluding the window bar.

    Args:
        canvas (tk.Canvas): Canvas to create window in.
        title (str): Window title.
        bbox (Tuple[int, int, int, int]): XYWH bounding box of window.

    Returns:
        tk.Frame: Frame widget to put window contents in.
    """
    x, y, w, h = bbox
    bar_h = 4 * EM

    # Create widgets.
    win = tk.Frame(canvas, bd=0, width=w, height=h + bar_h)
    content = tk.Frame(win, bd=2, relief="ridge")
    bar = tk.Frame(win, bd=2, bg="lightblue", relief="raised")
    tlabel = tk.Label(bar, text=title, font=f"Verdana {EM}", bg="lightblue")

    # Place widgets.
    bar.place(x=0, y=0, width=w, height=bar_h)
    content.place(x=0, y=bar_h, width=w, height=h)
    tlabel.pack(side="left")
    win_id = canvas.create_window((x, y), window=win, anchor="n")

    def _move_win(_):
        """Move window."""
        x0, y0 = canvas.winfo_pointerxy()
        x0 -= canvas.winfo_rootx()
        y0 -= canvas.winfo_rooty()
        canvas.coords(win_id, x0, y0)

    shaded = False

    def _shade_win(_):
        """Shade window."""
        nonlocal shaded
        if shaded := not shaded:
            content.place(height=0)
            win.configure(height=bar_h)
        else:
            content.place(height=h)
            win.configure(height=h + bar_h)

    # Move window on drag.
    bar.bind("<B1-Motion>", _move_win)
    tlabel.bind("<B1-Motion>", _move_win)

    # Shade window on double click.
    bar.bind("<Double-Button-1>", _shade_win)
    tlabel.bind("<Double-Button-1>", _shade_win)

    return content
