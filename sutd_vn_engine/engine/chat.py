"""Chat widget."""

import asyncio
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

from sutd_vn_engine.engine.utils import EM, LORUM

__all__ = ["ChatLog"]


class ChatLog(ttk.Labelframe):
    """Chat Log GUI."""

    def __init__(self, master=None, ncols=32, msgcols=22, **kwargs):
        """Constructor."""
        super(ChatLog, self).__init__(master, text="Chat Log", **kwargs)
        self.messages = []
        self.ncols = ncols
        self.msgcols = msgcols

        self.set_speaker("", "center")
        self._init_gui()
        self._init_style()

    def _init_gui(self):
        """Init GUI."""
        canvas = tk.Canvas(self, highlightthickness=0, bd=0, width=0, height=0)
        inner = tk.Frame(canvas, bd=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        canvas.config(yscrollcommand=scroll.set)
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.pack(fill="both", expand=True, side="left")
        scroll.pack(fill="y", side="right")

        def _on_canvas_configure(event):
            canvas.coords(inner_id, 0, 0)
            canvas.itemconfig(inner_id, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)

        self.canvas = canvas
        self.inner = inner
        self.scroll = scroll

    def _init_style(self):
        """Init style."""
        self.placement = dict(
            columnspan=self.msgcols,
            sticky="ew",
            padx=EM,
            pady=(0.3 * EM, 0.7 * EM),
        )
        self.style = ttk.Style(self)
        common = dict(relief="raised", padding=EM)

        def _on_inner_configure(event):
            cwidth = event.width // self.ncols
            common["wraplength"] = cwidth * self.msgcols - 4 * common["padding"]
            self.inner.columnconfigure([*range(self.ncols)], minsize=cwidth, weight=1)

            left = common | dict(background="white")
            right = common | dict(background="lightgreen")
            center = common | dict(background="lightblue", justify="center")

            self.style.configure("Left.TLabel", **left)
            self.style.configure("Right.TLabel", **right)
            self.style.configure("Center.TLabel", **center)

            self.canvas.config(scrollregion=(0, 0, 0, event.height))

        self.inner.bind("<Configure>", _on_inner_configure)

    def _msg(self, msg, name=None, side=None):
        """Common implementation for add_msg and add_anim_msg."""
        name = self.name if name is None else name
        side = self.side if side is None else side
        msg = f"{name}:\n{msg}" if name else msg

        row = len(self.messages)
        anchor = "center" if side == "center" else "w"
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

        message = ttk.Label(self.inner, style=style, anchor=anchor)
        textvar = tk.StringVar(message, value=msg)
        message.config(textvariable=textvar)
        message.grid(**self.placement, row=row, column=col)

        self.messages.append(dict(name=name, side=side, var=textvar, widget=message))
        return textvar, msg

    def add_msg(self, msg, name=None, side=None):
        """Add a message to the chat log."""
        self._msg(msg, name, side)
        self.update_idletasks()
        self.canvas.yview_moveto(1)

    async def add_anim_msg(self, msg, name=None, side=None, delay=0.01):
        """Add an message with typing animation to the chat log."""
        text, msg = self._msg(msg, name, side)

        cur = ""
        try:
            for c in msg:
                cur += c
                text.set(cur)
                await asyncio.sleep(delay)
                self.canvas.yview_moveto(1)
        except asyncio.CancelledError:
            pass
        finally:
            text.set(msg)
            self.update_idletasks()
            self.canvas.yview_moveto(1)

    def set_speaker(self, name=None, side=None):
        """Set the speaker name and side."""
        self.name = self.name if name is None else name
        self.side = self.side if side is None else side


if __name__ == "__main__":
    from pprint import pprint

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
