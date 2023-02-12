import requests
import tkinter as tk
from tkinter import messagebox

from utils import take_window_of_center, MAIN_URL_API


class DeckCreater:
    def __init__(
            self,
            token: str,
            window: tk.Tk
    ):
        self.token = token
        self.window = window
        self.new_window: tk.Toplevel = None
        self.create_deck_frame: tk.Frame = None
        self.deck_name: tk.Entry = None

    def create_deck_form(self):
        if self.create_deck_frame:
            self.create_deck_frame.destroy()
        self.new_window = tk.Toplevel()
        self.new_window.title('Создать колоду')
        win_width = 300
        win_height = 100
        center_width, center_height = take_window_of_center(win_width, win_height)
        self.new_window.geometry(f"{win_width}x{win_height}+{center_width}+{center_height}")
        self.create_deck_frame = tk.Frame(self.new_window)
        deck_name_label = tk.Label(self.create_deck_frame, text='Имя колоды')
        self.deck_name = tk.Entry(self.create_deck_frame)
        create_deck_button = tk.Button(
            self.create_deck_frame,
            text='Создать',
            command=self.create
        )

        deck_name_label.pack()
        self.deck_name.pack()
        create_deck_button.pack()
        self.create_deck_frame.pack()

    def create(self):
        deck_name = self.deck_name.get()
        create_new_deck = requests.post(
            url=f'{MAIN_URL_API}decks/create/',
            headers={
                'Authorization': f'Token {self.token}'
            },
            data={
                'name': deck_name,
            }
        )
        if create_new_deck.status_code == 200:
            messagebox.showinfo(message='Колода успешно создана')
            self.new_window.destroy()
        else:
            messagebox.showerror(message='При создании колоды произошла ошибка')
