"""Widget to display image."""

import logging
import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional

__all__ = ["Image"]

log = logging.getLogger(__name__)


class Image(tk.Button):
    """Is actually a button."""

    def __init__(self, master: Optional[tk.Misc] = None, img_fp: str = "", **kwargs):
        """Init."""
        self.img_fp = img_fp
        super(Image, self).__init__(master, **kwargs)
        self.img = tk.PhotoImage(master=self)
        self.config(image=self.img)
        try:
            self.img.config(file=img_fp)
        except tk.TclError:
            log.error(f"Image file not found: {img_fp}")

    def change_img(self, img_fp):
        """Change image."""
        self.img_fp = img_fp
        self.img.config(file=img_fp)
