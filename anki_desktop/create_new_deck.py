from tkinter import messagebox
import requests
import tkinter as tk
import customtkinter as ct
from utils import take_window_of_center, MAIN_URL_API
from pydantic_schemas import CreateDeckResult


class DeckCreater:
    def __init__(
            self,
            token: str,
            window: tk.Tk,
            study
    ):
        self.token = token
        self.window = window
        self.new_window: tk.Toplevel = None
        self.create_deck_frame: tk.Frame = None
        self.deck_name: ct.CTkEntry = None
        self.study = study

        self.error_message: tk.Label = None

    def create_deck_form(self):
        if self.create_deck_frame:
            self.create_deck_frame.destroy()
        self.new_window = tk.Toplevel()
        self.new_window.title('Создать колоду')
        win_width = 300
        win_height = 100
        center_width, center_height = take_window_of_center(
            win_width, win_height
            )
        self.new_window.geometry(
            f"{win_width}x{win_height}+{center_width}+{center_height}"
            )
        self.create_deck_frame = tk.Frame(self.new_window)
        deck_name_label = tk.Label(self.create_deck_frame, text='Имя колоды')
        self.deck_name = ct.CTkEntry(self.create_deck_frame)
        create_deck_button = ct.CTkButton(
            self.create_deck_frame,
            text='Создать',
            command=self.create
        )

        deck_name_label.grid(row=1, column=0)
        self.deck_name.grid(row=1, column=1, padx=5, pady=5)
        create_deck_button.grid(row=3, column=0, columnspan=2, pady=5)
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
        deck = CreateDeckResult.parse_obj(create_new_deck.json())
        if create_new_deck.status_code == 201:
            messagebox.showinfo(message=f'Колода {deck.name} успешно создана')
            self.new_window.destroy()
            self.study.show_decks()
        elif create_new_deck.status_code == 400:
            self.error_message = tk.Label(
                self.create_deck_frame, text=deck.name[0], fg='red'
                )
            self.error_message.pack()
        else:
            messagebox.showerror(
                message='При создании колоды произошла ошибка'
                )
