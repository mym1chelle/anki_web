import tkinter as tk
import customtkinter as ct
from requests.exceptions import ConnectionError
import requests
from tkinter import messagebox
from utils import (
    get_type_code,
    load_and_import_file,
    take_window_of_center,
    search_styles,
    search_deck,
    MAIN_URL_API
    )
from pydantic_schemas import Decks, Styles, CreateCardResult


class CardsCreater:
    def __init__(self, token, window, study):
        self.window = window
        self.token = token
        self.study = study

        self.__TYPE = ['Markdown', 'Text', 'HTML']
        all_decks = requests.get(
            url=f"{MAIN_URL_API}decks/",
            headers={
                'Authorization': f'Token {self.token}'
            }
        ).json()
        self.decks = Decks.parse_obj(all_decks)
        all_card_styles = requests.get(
            url=f"{MAIN_URL_API}styles/",
            headers={
                'Authorization': f'Token {self.token}'
            }
        ).json()
        self.styles = Styles.parse_obj(all_card_styles)
        
        if self.decks.results:
            self.names_of_decks = [deck.name for deck in self.decks.results]
        else:
            self.names_of_decks = [None]
        self.names_of_styles = [style.name for style in self.styles.styles]

        self.new_window: tk.Toplevel = None
        self.create_card_frame: tk.Frame = None
        self.import_cards_frame: tk.Frame = None

        self.card_question: ct.CTkTextbox = None
        self.card_question_error: tk.Label = None
        self.question_type: tk.StringVar = None
        self.card_answer: ct.CTkTextbox = None
        self.card_answer_error: tk.Label = None
        self.answer_type: tk.StringVar = None
        self.card_style: tk.StringVar = None
        self.deck_name: tk.StringVar = None

    def create_card(self):
        """Рендерит форму для создания карточки"""
        if self.create_card_frame:
            self.create_card_frame.destroy()
        if self.import_cards_frame:
            self.import_cards_frame.destroy()

        self.new_window = tk.Toplevel()
        self.new_window.title('Добавить карточку')
        win_width = 500
        win_height = 700
        center_width, center_height = take_window_of_center(
            win_width, win_height
            )
        self.new_window.geometry(
            f"{win_width}x{win_height}+{center_width}+{center_height}"
            )
        self.create_card_frame = tk.Frame(self.new_window)

        self.question_type = tk.StringVar()
        self.answer_type = tk.StringVar()
        self.card_style = tk.StringVar()
        self.deck_name = tk.StringVar()

        self.card_style.set(self.names_of_styles[0])
        self.deck_name.set(self.names_of_decks[0])
        self.question_type.set(self.__TYPE[1])
        self.answer_type.set(self.__TYPE[1])

        question_label = tk.Label(self.create_card_frame, text='Вопрос')
        self.card_question = ct.CTkTextbox(
            self.create_card_frame,
            width=win_width - 20
        )
        answer_label = tk.Label(self.create_card_frame, text='Ответ')
        self.card_answer = ct.CTkTextbox(
            self.create_card_frame,
            width=win_width - 20
        )

        question_type_label = tk.Label(
            self.create_card_frame, text='Тип вопроса'
            )
        selected_question_type = ct.CTkOptionMenu(
            values=self.__TYPE,
            master=self.create_card_frame,
            variable=self.question_type,
            width=105
        )

        answer_type_label = tk.Label(self.create_card_frame, text='Тип ответа')
        selected_answer_type = ct.CTkOptionMenu(
            master=self.create_card_frame,
            variable=self.answer_type,
            values=self.__TYPE,
            width=105
        )
        style_name_label = tk.Label(
            self.create_card_frame, text='Стиль карточки'
            )
        selected_style = ct.CTkOptionMenu(
            master=self.create_card_frame,
            variable=self.card_style,
            values=self.names_of_styles,
            width=140
        )
        deck_name_label = tk.Label(self.create_card_frame, text='Колода')
        select_deck_name = ct.CTkOptionMenu(
            master=self.create_card_frame,
            variable=self.deck_name,
            values=self.names_of_decks,
            width=105
        )
        create_card_button = ct.CTkButton(
            self.create_card_frame,
            text='Добавить',
            command=self.create
        )

        question_label.grid(row=0, column=0, columnspan=2)
        self.card_question.grid(row=1, column=0, columnspan=2, sticky="nsew")
        question_type_label.grid(row=2, column=0)
        selected_question_type.grid(row=2, column=1, pady=5)
        answer_label.grid(row=4, column=0, columnspan=2)
        self.card_answer.grid(row=5, column=0, columnspan=2)
        answer_type_label.grid(row=7, column=0)
        selected_answer_type.grid(row=7, column=1, pady=5)
        style_name_label.grid(row=8, column=0)
        selected_style.grid(row=8, column=1, pady=5)
        deck_name_label.grid(row=9, column=0)
        select_deck_name.grid(row=9, column=1, pady=5)
        create_card_button.grid(row=10, column=0, columnspan=2, pady=5)
        self.create_card_frame.pack()

    def create(self):
        if self.card_answer_error:
            self.card_answer_error.destroy()
        if self.card_question_error:
            self.card_question_error.destroy()
        """Процесс создания карточки"""
        name = self.deck_name.get()
        deck_id = search_deck(
            name=name,
            decks=self.decks)
        if deck_id:
            style_id = search_styles(
                name=self.card_style.get(),
                styles=self.styles
            )
            question = self.card_question
            if type(self.card_question) != str:
                question = self.card_question.get(index1='1.0', index2=tk.END)
            question_type_code = get_type_code(self.question_type.get())
            answer = self.card_answer
            if type(self.card_answer) != str:
                answer = self.card_answer.get(index1='1.0', index2=tk.END)
            answer_type_code = get_type_code(self.answer_type.get())
            try:
                create = requests.post(
                    url=f"{MAIN_URL_API}cards/create/",
                    data={
                        "question": question,
                        "question_type": question_type_code,
                        "answer": answer,
                        "answer_type": answer_type_code,
                        "style": style_id,
                        "deck": deck_id
                    },
                    headers={
                        'Authorization': f'Token {self.token}'
                    }
                )
                card = CreateCardResult.parse_obj(create.json())
                if create.status_code == 201:
                    self.new_window.destroy()
                    messagebox.showinfo(message='Карточка успешно создана')
                    self.study.show_decks()
                elif create.status_code == 400:
                    if card.question:
                        self.card_question_error = tk.Label(
                            self.create_card_frame,
                            text=card.question[0], fg='red'
                        )
                        self.card_question_error.grid(
                            row=3, column=0, columnspan=2)
                    if card.answer:
                        self.card_answer_error = tk.Label(
                            self.create_card_frame,
                            text=card.answer[0], fg='red'
                        )
                        self.card_answer_error.grid(
                            row=6, column=0, columnspan=2)
                else:
                    messagebox.showerror(message='При создании карточки произошла ошибка')
            except ConnectionError:
                messagebox.showerror(message='Неудалось подключиться к серверу')
        else:
            messagebox.showerror(message='У вас нет ни одной колоды')

    def import_cards(self):
        if self.create_card_frame:
            self.create_card_frame.destroy()
        if self.import_cards_frame:
            self.import_cards_frame.destroy()

        self.new_window = tk.Toplevel()
        self.new_window.title('Импортировать карточки')
        win_width = 300
        win_height = 250
        center_width, center_height = take_window_of_center(win_width, win_height)
        self.new_window.geometry(f"{win_width}x{win_height}+{center_width}+{center_height}")
        self.import_cards_frame = tk.Frame(self.new_window)

        question_type_label = tk.Label(self.import_cards_frame, text='Тип вопроса')
        self.question_type = tk.StringVar()
        answer_type_label = tk.Label(self.import_cards_frame, text='Тип ответа')
        self.answer_type = tk.StringVar()
        card_style_label = tk.Label(self.import_cards_frame, text='Стиль карточки')
        self.card_style = tk.StringVar()
        deck_label = tk.Label(self.import_cards_frame, text='Колода')
        self.deck_name = tk.StringVar()

        self.card_style.set(self.names_of_styles[0])
        self.deck_name.set(self.names_of_decks[0])
        self.question_type.set(self.__TYPE[1])
        self.answer_type.set(self.__TYPE[1])

        selected_question_type = ct.CTkOptionMenu(
            master=self.import_cards_frame,
            variable=self.question_type,
            values=self.__TYPE
        )
        selected_answer_type = ct.CTkOptionMenu(
            master=self.import_cards_frame,
            variable=self.answer_type,
            values=self.__TYPE
        )
        selected_style = ct.CTkOptionMenu(
            master=self.import_cards_frame,
            variable=self.card_style,
            values=self.names_of_styles
        )
        select_deck_name = ct.CTkOptionMenu(
            master=self.import_cards_frame,
            variable=self.deck_name,
            values=self.names_of_decks
        )

        select_file_button = ct.CTkButton(
            self.import_cards_frame,
            text='Выбрать файл',
            command=lambda: load_and_import_file(
                window=self.window,
                new_window=self.new_window,
                question_type_code=get_type_code(self.question_type.get()),
                answer_type_code=get_type_code(self.answer_type.get()),
                card_style=self.card_style.get(),
                styles=self.styles,
                deck_name=self.deck_name.get(),
                decks=self.decks,
                token=self.token,
                study=self.study
            )
        )

        question_type_label.grid(row=0, column=0)
        selected_question_type.grid(row=0, column=1, pady=5)
        answer_type_label.grid(row=1, column=0)
        selected_answer_type.grid(row=1, column=1, pady=5)
        card_style_label.grid(row=2, column=0)
        selected_style.grid(row=2, column=1, pady=5)
        deck_label.grid(row=3, column=0)
        select_deck_name.grid(row=3, column=1, pady=5)
        select_file_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.import_cards_frame.pack()


