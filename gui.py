import logging
import tkinter
import ttk
import async

PADDING = (5, 5, 5, 5)


class CardWidget:
    PROPERTIES = dict(width=60,
                      height=90,
                      borderwidth=1,
                      relief='sunken',
                      padding=PADDING)

    def __init__(self, parent):
        self.frame = ttk.Frame(parent, **self.PROPERTIES)
        self.frame.pack(side='left')
        self.value = None


def widget_descriptor(name):
    def fget(obj):
        return getattr(obj, name)['text']

    def fset(obj, val):
        getattr(obj, name)['text'] = val

    return property(fget, fset)


class PlayerWidget:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, borderwidth=1, relief='raised')
        self.name_label = ttk.Label(self.frame, text="Player")
        self.stack_label = ttk.Label(self.frame, text="0")
        self.bet_label = ttk.Label(self.frame, text="0")
        self.cards_frame = ttk.Frame(self.frame)
        self.cards_widgets = [CardWidget(self.cards_frame) for _ in range(2)]

        self.frame.pack(side='left')
        for w in [self.name_label, self.stack_label, self.bet_label, self.cards_frame]:
            w.pack()

    bet = widget_descriptor('bet_label')
    stack = widget_descriptor('stack_label')
    name = widget_descriptor('name')

    @property
    def cards(self):
        return [w.value for w in self.cards_widgets]

    @cards.setter
    def cards(self, val):
        for v, c in zip(val, self.cards_widgets):
            c.value = v


class MainWidow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.server = None
        self.show_settings_window()
        self.root.protocol('WM_DELETE_WINDOW', async.stop)

    def show_settings_window(self):
        self.settings_window = tkinter.Toplevel(self.root)

        self.settings_window.protocol('WM_DELETE_WINDOW', self.root.destroy)
        self.root.withdraw()

        login_label = ttk.Label(self.settings_window, text="Name:")
        self.login_input = ttk.Entry(self.settings_window)
        self.login_input.insert(0, "User")

        address_label = ttk.Label(self.settings_window, text="Address:")
        self.address_input = ttk.Entry(self.settings_window)
        self.address_input.insert(0, "sorseg.ru")

        connect = ttk.Button(self.settings_window, text="Connect", command=self.connect)
        serve = ttk.Button(self.settings_window, text="Serve", command=self.serve)

        login_label.grid(row=0, column=0)
        self.login_input.grid(row=0, column=1)
        address_label.grid(row=1, column=0)
        self.address_input.grid(row=1, column=1)
        connect.grid(row=2, column=0)
        serve.grid(row=3, column=0)

    def take_a_seat(self):
        return PlayerWidget(self.opponents_frame)

    def make_board(self):
        self.status = ttk.Label(self.root)
        self.status.pack()
        self.opponents_frame = ttk.Frame(self.root, padding=PADDING)
        self.opponents_frame.pack()

        self.table_frame = ttk.Frame(self.root, padding=PADDING)
        self.table_frame.pack()
        table_label = ttk.Label(self.table_frame, text="Table:", padding=PADDING)
        table_label.pack(side='left')
        self.card_widgets = [CardWidget(self.table_frame) for _ in range(5)]

        self.cards_frame = ttk.Frame(self.root, padding=PADDING)
        cards_label = ttk.Label(self.cards_frame, text="Your cards:", padding=PADDING)
        cards_label.pack(side='left')
        self.my_card_widgets = [CardWidget(self.cards_frame) for _ in range(2)]
        self.cards_frame.pack()
        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack()
        self.deal_button = ttk.Button(self.buttons_frame, text="Deal", command=self.deal)
        self.deal_button.pack(side='left')

        self.check_button = ttk.Button(self.buttons_frame, text="Check", command=self.check)
        self.check_button.pack(side='left')

        self.check_button = ttk.Button(self.buttons_frame, text="Check", command=self.check)
        self.check_button.pack(side='left')

    def serve(self):
        self.settings_window.withdraw()
        self.root.deiconify()
        async.create_server()
        self.make_board()
        self.status['text'] = 'Waiting for players...'

    def connect(self):
        pass

    def deal(self):
        pass

    def check(self):
        pass


window = MainWidow()


def main():
    logging.info("Starting tkinter")
    window.root.mainloop()
    logging.info("Tkinter stopped")