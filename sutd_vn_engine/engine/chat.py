"""Chat widget."""

from tkinter import *
from tkinter.ttk import *  # type: ignore

__all__ = ["ChatLog"]

EM = 8  # In px.


class ChatLog(Labelframe):
    """Chat Log GUI."""

    def __init__(self, master=None, ncols=32, msgcols=18, colwidth=2 * EM):
        """Constructor."""
        super(ChatLog, self).__init__(master=master, text="Chat Log")
        self.messages = []
        self.ncols = ncols
        self.msgcols = msgcols
        self.colwidth = colwidth

        self.set_speaker("", CENTER)
        self.init_gui()
        self.init_style()

    def init_gui(self):
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

    def init_style(self):
        """Init style."""
        self.style = Style(self)
        common = dict(
            relief=RAISED,
            wraplength=self.msgcols * self.colwidth,
            padding=0.5 * EM,
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
            pady=(0.5 * EM, 1.5 * EM),
        )

    def update_inner_size(self):
        """Update size of inner canvas for scrolling."""
        height = 0
        for m in self.messages:
            widget = m["widget"]
            pad = widget.grid_info()["pady"]
            height += widget.winfo_reqheight()
            height += pad if isinstance(pad, int) else sum(pad)
        self.canvas.config(scrollregion=(0, 0, 0, height))

    def set_speaker(self, name=None, side=None):
        """Set the speaker name and side."""
        self.name = self.name if name is None else name
        self.side = self.side if side is None else side

    def add_message(self, msg, name=None, side=None):
        """Add a message to the chat log."""
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

        message = Label(self.inner, text=msg, style=style, anchor=anchor)
        message.grid(**self.placement, row=row, column=col)

        self.messages.append(dict(name=name, msg=msg, side=side, widget=message))
        self.update_inner_size()


if __name__ == "__main__":
    from pprint import pprint

    root = Tk()
    root.title("Chat Log Test")
    root.configure(bg="pink")
    root.geometry("800x600")
    root.resizable(width=False, height=False)

    chatlog = ChatLog(root)
    chatlog.pack(fill=Y, expand=True)

    lorum = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at "
        "elit non orci luctus porta et sit amet turpis. Vestibulum magna velit, "
        "finibus vel luctus vitae, condimentum eleifend diam. Maecenas ultrices "
        "neque at orci porta, a gravida eros aliquam. Phasellus eget ex placerat, "
        "condimentum nunc eget, convallis ante. Quisque feugiat magna massa, sit "
        "amet consectetur velit iaculis non. Aliquam nec."
    )

    chatlog.add_message("This is the beginning of the conversation.")

    chatlog.set_speaker("You", RIGHT)
    chatlog.add_message("Hello, world! Why is this being split across two lines?")
    chatlog.add_message(lorum)

    chatlog.set_speaker("Someone Else", LEFT)
    chatlog.add_message(lorum)
    chatlog.add_message(lorum)
    chatlog.add_message(lorum)

    pprint(chatlog.messages)
    root.mainloop()
