"""Utility for creating windowed frames in a canvas."""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Tuple
from uuid import uuid4

from .utils import EM, add_bind_tag

__all__ = ["create_window"]

WIN_TAG = "Window"
"""Canvas tag for all windowed frames."""


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
    bar_h = 4 * EM  # Height of window bar.
    grip_s = 1.5 * EM  # Size of window grip.
    shaded = False  # Whether window is shaded.

    # Add/retrieve map of canvas ids to windowed frames to canvas.
    win_id_map: Dict[int, tk.Frame] = getattr(canvas, "win_id_map", {})
    setattr(canvas, "win_id_map", win_id_map)

    # Create widgets.
    win = tk.Frame(canvas, bd=0, width=w, height=h + bar_h)
    content = tk.Frame(win, bd=2, relief="ridge")
    bar = tk.Frame(win, bd=2, bg="lightblue", relief="raised")
    tlabel = tk.Label(bar, text=title, font=f"Verdana {EM}", bg="lightblue")
    grip = ttk.Sizegrip(win)

    def _layout_widgets():
        """Layout widgets in a function to allow resizing later."""
        bar.place(x=0, y=0, width=w, height=bar_h)
        content.place(x=0, y=bar_h, width=w, height=h)
        grip.place(
            x=w - grip_s - 2, y=h + bar_h - grip_s - 2, width=grip_s, height=grip_s
        )

    _layout_widgets()
    tlabel.pack(side="left")
    win_id = canvas.create_window((x, y), window=win, anchor="nw", tags=WIN_TAG)

    # Add window to id map.
    win_id_map[win_id] = win

    def _move_win(_):
        """Move window."""
        nonlocal x, y
        x, y = canvas.winfo_pointerxy()
        x -= canvas.winfo_rootx()
        y -= canvas.winfo_rooty()
        # Add some additional offsets to center window bar on cursor.
        x -= w // 2
        y -= bar_h // 2
        canvas.coords(win_id, x, y)

    def _shade_win(_):
        """Shade window."""
        nonlocal shaded
        if shaded := not shaded:
            content.place(height=0)
            win.config(height=bar_h)
        else:
            content.place(height=h)
            win.config(height=h + bar_h)

    def _raise_win(_):
        """Raise window."""
        # Get click coords.
        cx, cy = canvas.winfo_pointerxy()
        cx -= canvas.winfo_rootx()
        cy -= canvas.winfo_rooty()

        # Get all windows within click coords and their stack order.
        wins = []
        for wid, win in win_id_map.items():
            # Get window bounds.
            x1, y1, x2, y2 = canvas.bbox(wid)
            if x1 < cx < x2 and y1 < cy < y2:
                # Get window stack order.
                order = canvas.winfo_children().index(win)
                wins.append((order, win))

        # Raise the topmost window under click.
        if wins:
            _, win = max(wins, key=lambda x: x[0])
            win.tkraise()

    def _resize_win(_):
        """Resize window."""
        nonlocal w, h
        # Get click coords.
        cx, cy = canvas.winfo_pointerxy()
        cx -= canvas.winfo_rootx()
        cy -= canvas.winfo_rooty()

        # New width & height.
        w, h = max(cx - x, bar_h + EM), max(cy - y - bar_h, bar_h + EM)

        # Resize window by placing widgets again.
        win.config(width=w, height=h + bar_h)
        _layout_widgets()

    # Add bind tag for window bar.
    bar_tag = uuid4().hex
    add_bind_tag(bar_tag, bar, tlabel)

    # NOTE: `bind_class` and `bind_all` act & persist on a global level, regardless
    # of the widget they are called on.

    # Move window on drag.
    win.bind_class(bar_tag, "<B1-Motion>", _move_win)

    # Shade window on double click.
    win.bind_class(bar_tag, "<Double-Button-1>", _shade_win)

    # Raise window on click.
    # NOTE: This handler is overwritten each time. It's fine.
    win.bind_all("<Button-1>", _raise_win, "+")

    # Remove default bind tags from grip to prevent default resizing.
    grip.bindtags((str(grip), ".", "all"))
    # Resize window on dragging grip.
    grip.bind("<B1-Motion>", _resize_win)

    # Remove window from id map on destroy.
    win.bind("<Destroy>", lambda _: win_id_map.pop(win_id, None))

    return content
