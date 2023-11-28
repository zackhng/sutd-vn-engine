"""ChatLog widget."""

import asyncio
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from typing import List, Literal, Optional, TypeAlias

from sutd_vn_engine.engine.utils import EM, LORUM

__all__ = ["ChatLog", "_MsgSide"]


_MsgSide: TypeAlias = Literal["left", "right", "center"]
"""Positions message can be placed in ChatLog."""


class ChatLog(ttk.Labelframe):
    """ChatLog widget."""

    def __init__(
        self,
        master: Optional[tk.Misc] = None,
        ncols: int = 32,
        msgcols: int = 22,
        **kwargs,
    ):
        """Create ChatLog widget.

        Args:
            master (Optional[tk.Misc], optional): Master widget. Defaults to None.
            ncols (int, optional): Number of columns total. Defaults to 32.
            msgcols (int, optional): Column span of messages. Defaults to 22.
            **kwargs: Keyword arguments for ttk.Labelframe.
        """
        super(ChatLog, self).__init__(master, text="Chat Log", **kwargs)
        self.messages: List[dict] = []
        self.ncols = ncols
        self.msgcols = msgcols

        self.name = ""
        self.side: _MsgSide = "center"

        self._init_gui()
        self._init_style()

    def _init_gui(self):
        """Init GUI."""
        # Create widgets.
        canvas = tk.Canvas(self, highlightthickness=0, bd=0, width=0, height=0)
        inner = tk.Frame(canvas, bd=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        # Configure scrollbar for canvas.
        canvas.config(yscrollcommand=scroll.set)

        # Place widgets.
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.pack(fill="both", expand=True, side="left")
        scroll.pack(fill="y", side="right")

        def _on_canvas_configure(event: tk.Event):
            """Update inner frame size when canvas is resized."""
            canvas.coords(inner_id, 0, 0)
            canvas.itemconfig(inner_id, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)

        self.canvas = canvas
        self.inner = inner
        self.scroll = scroll

    def _init_style(self):
        """Init style."""
        self.style = ttk.Style(self)

        # Common style for all messages.
        common = dict(relief="raised", padding=EM)

        # Common grid placement properties for messages.
        self.placement = dict(
            columnspan=self.msgcols,
            sticky="ew",
            padx=EM,
            pady=(0.3 * EM, 0.7 * EM),
        )

        def _on_inner_configure(event: tk.Event):
            """Update message wrap & canvas scroll area when inner frame is resized."""
            cwidth = event.width // self.ncols
            common["wraplength"] = cwidth * self.msgcols - 4 * common["padding"]
            self.inner.columnconfigure([*range(self.ncols)], minsize=cwidth, weight=1)

            # Position specific styles for messages.
            left = common | dict(background="white")
            right = common | dict(background="lightgreen")
            center = common | dict(background="lightblue", justify="center")

            # Update styles.
            self.style.configure("Left.TLabel", **left)
            self.style.configure("Right.TLabel", **right)
            self.style.configure("Center.TLabel", **center)

            # Update canvas scroll area.
            self.canvas.config(scrollregion=(0, 0, 0, event.height))

        self.inner.bind("<Configure>", _on_inner_configure)

    def _msg(
        self, msg: str, name: Optional[str] = None, side: Optional[_MsgSide] = None
    ):
        """Common implementation for add_msg and add_anim_msg.

        Set `name` and `side` to temporarily override the current speaker & position.

        Args:
            msg (str): Message to add.
            name (Optional[str], optional): Name of speaker. Defaults to None.
            side (Optional[_MsgSide], optional): Position of message. Defaults to None.

        Returns:
            Tuple[tk.StringVar, str]: Text variable, full message.
        """
        name = self.name if name is None else name
        side = self.side if side is None else side
        msg = f"{name}:\n{msg}" if name else msg

        # Calculate grid placement & style of message.
        row = len(self.messages)
        anchor: tk._Anchor = "center" if side == "center" else "w"
        if side == "left":
            col = 0
            style = "Left.TLabel"
        elif side == "right":
            col = self.ncols - self.msgcols
            style = "Right.TLabel"
        elif side == "center":
            col = (self.ncols - self.msgcols) // 2
            style = "Center.TLabel"
        else:
            raise ValueError(f"Side {side} not supported.")

        # Create & configure message.
        message = ttk.Label(self.inner, style=style, anchor=anchor)
        textvar = tk.StringVar(message, value=msg)
        message.config(textvariable=textvar)
        message.grid(**self.placement, row=row, column=col)

        self.messages.append(dict(name=name, side=side, var=textvar, widget=message))
        return textvar, msg

    def add_msg(
        self, msg: str, name: Optional[str] = None, side: Optional[_MsgSide] = None
    ):
        """Add a message to the chat log synchronously.

        Set `name` and `side` to temporarily override the current speaker & position.

        Args:
            msg (str): Message to add.
            name (Optional[str], optional): Name of speaker. Defaults to None.
            side (Optional[_MsgSide], optional): Position of message. Defaults to None.
        """
        self._msg(msg, name, side)

        # Scroll canvas to bottom.
        self.update_idletasks()  # Recompute inner frame size first.
        self.canvas.yview_moveto(1)

    async def add_anim_msg(
        self,
        msg: str,
        name: Optional[str] = None,
        side: Optional[_MsgSide] = None,
        delay: int = 10,
    ):
        """Add a message to the chat log asynchronously with typing animation.

        Set `name` and `side` to temporarily override the current speaker & position.

        Args:
            msg (str): Message to add.
            name (Optional[str], optional): Name of speaker. Defaults to None.
            side (Optional[_MsgSide], optional): Position of message. Defaults to None.
            delay (int, optional): Delay between each character in ms. Defaults to 10.
        """
        text, msg = self._msg(msg, name, side)

        cur = ""
        try:
            # Animate typing character by character.
            for c in msg:
                cur += c
                text.set(cur)
                await asyncio.sleep(delay / 1000)
                self.canvas.yview_moveto(1)
        except asyncio.CancelledError:
            pass
        finally:
            # Set full message & scroll to bottom when done or cancelled.
            text.set(msg)
            self.update_idletasks()
            self.canvas.yview_moveto(1)

    def set_speaker(self, name: Optional[str] = None, side: Optional[_MsgSide] = None):
        """Set the name & position for subsequent messages.

        If left as None, the current value will remain unchanged.

        Args:
            name (Optional[str], optional): Name of speaker. Defaults to None.
            side (Optional[MsgSide], optional): Position of message. Defaults to None.
        """
        self.name = self.name if name is None else name
        self.side = self.side if side is None else side


# Test ChatLog widget.
if __name__ == "__main__":
    from pprint import pprint

    # Create and configure window.
    root = tk.Tk()
    root.title("Chat Log Test")
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.config(family="Courier New", size=EM)
    root.option_add("*Font", default_font)
    root.config(bg="pink")
    root.geometry("1280x960")
    root.resizable(width=False, height=False)

    chatlog = ChatLog(root)
    chatlog.pack(fill="both", expand=True)

    pad = True

    def _resize(_):
        """Resize ChatLog on click by changing padding."""
        global pad
        if pad := not pad:
            chatlog.pack(padx=20 * EM)
        else:
            chatlog.pack(padx=10 * EM)

    _resize(None)
    chatlog.bind("<Button-1>", _resize)

    def _test():
        chatlog.add_msg("This is the beginning of the conversation.")

        chatlog.set_speaker("You", "right")
        chatlog.add_msg("Hello, world! Why is this being split across two lines?")
        chatlog.add_msg(LORUM)

        chatlog.set_speaker("Someone Else", "left")
        chatlog.add_msg(LORUM)
        chatlog.add_msg(LORUM)
        chatlog.add_msg(LORUM)

        pprint(chatlog.messages)

    root.after(500, _test)
    root.mainloop()
