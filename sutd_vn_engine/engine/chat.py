"""Chat widget."""

import asyncio
from tkinter import *
from tkinter.ttk import *  # type: ignore

from sutd_vn_engine.engine.utils import EM, LORUM

__all__ = ["ChatLog"]


class ChatLog(Labelframe):
    """Chat Log GUI."""

    def __init__(self, master=None, ncols=32, msgcols=22, colwidth=3 * EM):
        """Constructor."""
        super(ChatLog, self).__init__(master=master, text="Chat Log")
        self.messages = []
        self.ncols = ncols
        self.msgcols = msgcols
        self.colwidth = colwidth

        self.set_speaker("", CENTER)
        self._init_gui()
        self._init_style()

    def _init_gui(self):
        """Init GUI."""
        canvas = Canvas(self, width=(self.ncols + 2) * self.colwidth)
        inner = Frame(canvas)
        scroll = Scrollbar(self, orient=VERTICAL, command=canvas.yview)

        canvas.config(yscrollcommand=scroll.set)
        canvas.create_window((canvas.winfo_reqwidth() / 2, 0), window=inner, anchor=N)
        inner.columnconfigure(list(range(self.ncols)), minsize=self.colwidth, weight=0)

        canvas.pack(fill=BOTH, expand=True, side=LEFT)
        scroll.pack(fill=Y, side=RIGHT)

        self.canvas = canvas
        self.inner = inner
        self.scroll = scroll

    def _init_style(self):
        """Init style."""
        self.style = Style(self)
        common = dict(
            relief=RAISED,
            wraplength=self.msgcols * self.colwidth,
            padding=EM,
        )
        left = common | dict(background="white")
        right = common | dict(background="lightgreen")
        center = common | dict(background="lightblue", justify=CENTER)
        self.style.configure("Left.TLabel", **left)
        self.style.configure("Right.TLabel", **right)
        self.style.configure("Center.TLabel", **center)

        self.placement = dict(
            columnspan=self.msgcols,
            sticky=EW,
            pady=(0.3 * EM, 0.7 * EM),
        )

    def _calc_msg_height(self, msgdict):
        """Calculate height of message."""
        widget = msgdict["widget"]
        padinfo = widget.grid_info()["pady"]
        pad = padinfo if isinstance(padinfo, int) else sum(padinfo)
        return widget.winfo_reqheight() + pad

    def _update_scroll(self):
        """Update size of inner canvas for scrolling."""
        height = 0
        for m in self.messages:
            height += m["height"]
        self.canvas.config(scrollregion=(0, 0, 0, height))
        self.canvas.yview_moveto(1)

    def _msg(self, msg, name=None, side=None):
        """Common implementation for add_msg and add_anim_msg."""
        name = self.name if name is None else name
        side = self.side if side is None else side
        msg = f"{name}:\n{msg}" if name else msg

        row = len(self.messages)
        anchor = CENTER if side == CENTER else W
        if side == LEFT:
            col = 0
            style = "Left.TLabel"
        elif side == RIGHT:
            col = self.ncols - self.msgcols
            style = "Right.TLabel"
        elif side == CENTER:
            col = (self.ncols - self.msgcols) // 2
            style = "Center.TLabel"
        else:
            raise ValueError(f"Side {side} not supported.")

        textvar = StringVar(value=msg)
        message = Label(self.inner, textvariable=textvar, style=style, anchor=anchor)
        message.grid(**self.placement, row=row, column=col)
        height = self._calc_msg_height(dict(widget=message))

        self.messages.append(
            dict(name=name, side=side, height=height, var=textvar, widget=message)
        )
        self._update_scroll()
        return textvar, msg

    def add_msg(self, msg, name=None, side=None):
        """Add a message to the chat log."""
        self._msg(msg, name, side)

    async def add_anim_msg(self, msg, name=None, side=None, delay=0.01):
        """Add an message with typing animation to the chat log."""
        text, msg = self._msg(msg, name, side)

        cur = ""
        try:
            for c in msg:
                cur += c
                text.set(cur)
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            pass
        finally:
            text.set(msg)

    def set_speaker(self, name=None, side=None):
        """Set the speaker name and side."""
        self.name = self.name if name is None else name
        self.side = self.side if side is None else side


if __name__ == "__main__":
    from pprint import pprint

    root = Tk()
    root.title("Chat Log Test")
    root.configure(bg="pink")
    root.geometry("1280x960")
    root.resizable(width=False, height=False)

    chatlog = ChatLog(root)
    chatlog.pack(fill=Y, expand=True)

    chatlog.add_msg("This is the beginning of the conversation.")

    chatlog.set_speaker("You", RIGHT)
    chatlog.add_msg("Hello, world! Why is this being split across two lines?")
    chatlog.add_msg(LORUM)

    chatlog.set_speaker("Someone Else", LEFT)
    chatlog.add_msg(LORUM)
    chatlog.add_msg(LORUM)
    chatlog.add_msg(LORUM)

    pprint(chatlog.messages)
    root.mainloop()
