import tkinter as tk
import requests
from tkinter import messagebox
from utils import get_type_code, load_and_import_file, take_window_of_center, MAIN_URL_API, search_styles, search_deck
from pydantic_models import Decks, Styles


class CardsCreater:
    def __init__(self, token, window):
        self.window = window
        self.token = token
        self.__TYPE = ['Markdown', 'Text', 'HTML']

        self.decks = None
        all_decks = requests.get(
            url=f"{MAIN_URL_API}decks/",
            headers={
                'Authorization': f'Token {self.token}'
            }
        ).json()
        self.decks = Decks.parse_obj(all_decks)
        if self.decks.decks:
            self.names_of_decks = [deck.name for deck in self.decks.decks]
        else:
            self.names_of_decks = [None]

        all_card_styles = requests.get(
            url=f"{MAIN_URL_API}styles/",
            headers={
                'Authorization': f'Token {self.token}'
            }
        ).json()
        self.styles = Styles.parse_obj(all_card_styles)
        self.names_of_styles = [style.name for style in self.styles.styles]

        self.new_window: tk.Toplevel = None
        self.create_card_frame: tk.Frame = None
        self.import_cards_frame: tk.Frame = None

        self.card_question: tk.Entry = None
        self.question_type: tk.StringVar = None
        self.card_answer: tk.Entry = None
        self.answer_type: tk.StringVar = None
        self.card_style: tk.StringVar = None
        self.deck_name: tk.StringVar = None

    def create_card(self):
        if self.create_card_frame:
            self.create_card_frame.destroy()
        if self.import_cards_frame:
            self.import_cards_frame.destroy()

        self.new_window = tk.Toplevel()
        self.new_window.title('Добавить карточку')
        win_width = 300
        win_height = 200
        center_width, center_height = take_window_of_center(win_width, win_height)
        self.new_window.geometry(f"{win_width}x{win_height}+{center_width}+{center_height}")
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
        self.card_question = tk.Entry(self.create_card_frame)
        answer_label = tk.Label(self.create_card_frame, text='Ответ')
        self.card_answer = tk.Entry(self.create_card_frame)
        selected_question_type = tk.OptionMenu(
            self.create_card_frame,
            self.question_type,
            *self.__TYPE
        )
        selected_answer_type = tk.OptionMenu(
            self.create_card_frame,
            self.answer_type,
            *self.__TYPE
        )
        selected_style = tk.OptionMenu(
            self.create_card_frame,
            self.card_style,
            *self.names_of_styles
        )
        select_deck_name = tk.OptionMenu(
            self.create_card_frame,
            self.deck_name,
            *self.names_of_decks
        )
        create_card_button = tk.Button(
            self.create_card_frame,
            text='Добавить',
            command=self.create
        )

        question_label.grid(row=0, column=0, columnspan=2)
        self.card_question.grid(row=1, column=0)
        selected_question_type.grid(row=1, column=1)
        answer_label.grid(row=2, column=0, columnspan=2)
        self.card_answer.grid(row=3, column=0)
        selected_answer_type.grid(row=3, column=1)
        selected_style.grid(row=4, column=0)
        select_deck_name.grid(row=4, column=1)
        create_card_button.grid(row=5, column=0, columnspan=2)
        self.create_card_frame.pack()

    def create(self):
        deck_id = search_deck(
            name=self.deck_name.get(),
            decks=self.decks)
        if deck_id:
            style_id = search_styles(
                name=self.card_style.get(),
                styles=self.styles
            )
            question = self.card_question
            if type(self.card_question) != str:
                question = self.card_question.get()
            question_type_code = get_type_code(self.question_type.get())
            answer = self.card_answer
            if type(self.card_answer) != str:
                answer = self.card_answer.get()
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
                if create.status_code == 201:
                    messagebox.showinfo(message='Карточка успешно создана')
                    self.create_card_frame.destroy()
                    self.new_window.destroy()
                else:
                    messagebox.showerror(message='При создании карточки произошла ошибка')
            except:
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
        win_height = 100
        center_width, center_height = take_window_of_center(win_width, win_height)
        self.new_window.geometry(f"{win_width}x{win_height}+{center_width}+{center_height}")
        self.import_cards_frame = tk.Frame(self.new_window)
        self.question_type = tk.StringVar()
        self.answer_type = tk.StringVar()
        self.card_style = tk.StringVar()
        self.deck_name = tk.StringVar()
        self.card_style.set(self.names_of_styles[0])
        self.deck_name.set(self.names_of_decks[0])
        self.question_type.set(self.__TYPE[1])
        self.answer_type.set(self.__TYPE[1])

        selected_question_type = tk.OptionMenu(
            self.import_cards_frame,
            self.question_type,
            *self.__TYPE
        )
        selected_answer_type = tk.OptionMenu(
            self.import_cards_frame,
            self.answer_type,
            *self.__TYPE
        )
        selected_style = tk.OptionMenu(
            self.import_cards_frame,
            self.card_style,
            *self.names_of_styles
        )
        select_deck_name = tk.OptionMenu(
            self.import_cards_frame,
            self.deck_name,
            *self.names_of_decks
        )
        select_file_button = tk.Button(
            self.import_cards_frame,
            text='Импортировать',
            command=lambda: load_and_import_file(
                window=self.window,
                new_window=self.new_window,
                question_type_code=get_type_code(self.question_type.get()),
                answer_type_code=get_type_code(self.answer_type.get()),
                card_style_id=self.names_all_card_styles.get(self.card_style.get()),
                deck_id=self.names_all_decks.get(self.deck_name.get()),
                token=self.token
            )
        )

        selected_question_type.grid(row=0, column=0)
        selected_answer_type.grid(row=0, column=1)
        selected_style.grid(row=1, column=0)
        select_deck_name.grid(row=1, column=1)
        select_file_button.grid(row=2, column=0, columnspan=2)
        self.import_cards_frame.pack()


