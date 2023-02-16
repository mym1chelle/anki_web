import tkinter as tk
from tkinter import ttk
import customtkinter as ct
import requests
from supermemo2 import SMTwo
from tkhtmlview import HTMLLabel
from pydantic_schemas import GetCardToday, GetCardAnswer
from utils import BG_COLOR, MAIN_URL_API, win_height, TEXT_COLOR


class CardsForStudy:
    def __init__(self, window, token):
        self.window = window
        self.token = token

        self.study_card_frame: tk.Frame = None
        self.show_study_decks_frame: tk.Frame = None

        self.show_answer_button: tk.Button = None

    def hidden_decks_and_cards(self):
        if self.show_study_decks_frame:
            self.show_study_decks_frame.destroy()
        if self.study_card_frame:
            self.study_card_frame.destroy()

    def show_decks(self):
        if self.show_study_decks_frame:
            self.show_study_decks_frame.destroy()
        if self.study_card_frame:
            self.study_card_frame.destroy()
        study = requests.get(
            url=f'{MAIN_URL_API}decks/daily/',
            headers={
                'Authorization': f'Token {self.token}'
            }
        )
        self.show_study_decks_frame = tk.Frame(self.window)
        if study:
            style = ttk.Style()
            style.theme_use()
            style.configure(
                'Treeview',
                background=BG_COLOR,
                foreground=TEXT_COLOR,
                rowheight=25,
                fieldbackground=MAIN_URL_API,
            )
            decks_ = ttk.Treeview(self.show_study_decks_frame, height=win_height)
            decks_['columns'] = (
                'deck',
                'new',
                'repeat'
            )
            decks_.column("#0", width=0,  stretch=tk.NO)
            decks_.column("deck", anchor=tk.CENTER, width=180)
            decks_.column("new", anchor=tk.CENTER, width=180)
            decks_.column("repeat", anchor=tk.CENTER, width=180)

            decks_.heading("#0", text="", anchor=tk.CENTER)
            decks_.heading("deck", text="Колода", anchor=tk.CENTER)
            decks_.heading("new", text="Новые", anchor=tk.CENTER)
            decks_.heading("repeat", text="Повтор", anchor=tk.CENTER)

            for num, deck in enumerate(study.json()):
                decks_.insert(
                    parent='', index='end', iid=num, text='',
                    values=(deck['name'], deck['new_cards'], deck['old_cards'], deck['id'])
                )

                def select_record(a):
                    selected = decks_.focus()
                    values = decks_.item(selected, 'values')
                    if values:
                        self.study(deck_id=int(values[3]))

                decks_.bind("<Double-1>", select_record)
                decks_.grid(pady=15)
                self.show_study_decks_frame.pack()

    def study(self, deck_id: int):
        self.hidden_decks_and_cards()
        self.study_card_frame = tk.Frame(self.window, height=100)
        get_today_card = requests.get(
            url=f"{MAIN_URL_API}decks/{deck_id}/cards/",
            headers={
                'Authorization': f'Token {self.token}'
            }
        )
        if get_today_card.status_code == 200:
            card = GetCardToday.parse_obj(get_today_card.json())
            count = card.count
            if card.results:
                card_data = card.results[0]
                cards_count = tk.Label(self.study_card_frame, text=f'Осталось: {count}')
                cards_count.grid(row=1, column=0, columnspan=5)
                if card_data.question_type == 'text':
                    card_question = ct.CTkTextbox(self.study_card_frame, width=570, fg_color=BG_COLOR)
                    card_question.tag_config("tag_name", justify='center')
                    card_question.insert('1.0', text=card_data.question)
                    card_question.tag_add("tag_name", "1.0", "end")
                    card_question.configure(state='disabled')
                elif card_data.question_type == 'html':
                    card_question = HTMLLabel(
                        self.study_card_frame,
                        background=BG_COLOR,
                        html=card_data.question,
                    )
                card_question.grid(row=2, column=0, columnspan=5)
                self.show_answer_button = tk.Button(
                        self.study_card_frame,
                        text='Ответ',
                        command=lambda: self.show_answer(answer=card_data.answer, card_id=card_data.id, deck_id=deck_id)
                        )
                self.show_answer_button.grid(row=3, column=0, columnspan=5)
                self.study_card_frame.pack()
            else:
                no_cards = tk.Label(self.study_card_frame, text='На сегодня все')
                no_cards.grid(row=1, column=0, columnspan=5)
                self.study_card_frame.pack()

    def show_answer(self, answer: str, card_id: int, deck_id: int):
        self.show_answer_button.grid_forget()
        separator = ttk.Separator(self.study_card_frame, orient=tk.HORIZONTAL)
        take_answer = ct.CTkTextbox(self.study_card_frame, width=570, fg_color=BG_COLOR)
        take_answer.tag_config("tag_name", justify='center')
        take_answer.insert('1.0', answer)
        take_answer.tag_add("tag_name", "1.0", "end")
        take_answer.configure(state='disabled')
        # take_answer = HTMLLabel(self.study_card_frame, html=f"<p>{answer}</p>")
        button_one = tk.Button(
            self.study_card_frame, text='Очень сложно',
            fg='red',
            command=lambda: self.change_card(
                rating=1,
                card_id=card_id,
                token=self.token,
                deck_id=deck_id
            )
        )
        button_two = tk.Button(
            self.study_card_frame,
            fg='orange',
            text='Сложно',
            command=lambda: self.change_card(
                rating=2,
                card_id=card_id,
                token=self.token,
                deck_id=deck_id
            )
        )
        button_three = tk.Button(
            self.study_card_frame,
            text='Норм',
            command=lambda: self.change_card(
                rating=3,
                card_id=card_id,
                token=self.token,
                deck_id=deck_id
            )
        )
        button_four = tk.Button(
            self.study_card_frame,
            fg='blue',
            text='Легко',
            command=lambda: self.change_card(
                rating=4,
                card_id=card_id,
                token=self.token,
                deck_id=deck_id
            )
        )
        button_five = tk.Button(
            self.study_card_frame,
            fg='green',
            text='Очень легко',
            command=lambda: self.change_card(
                rating=5,
                card_id=card_id,
                token=self.token,
                deck_id=deck_id
            )
        )
        separator.grid(row=4, column=0, columnspan=5, ipadx=300, pady=15)
        take_answer.grid(row=5, column=0, columnspan=5, pady=5)
        button_one.grid(row=6, column=0)
        button_two.grid(row=6, column=1)
        button_three.grid(row=6, column=2)
        button_four.grid(row=6, column=3)
        button_five.grid(row=6, column=4)

    def change_card(self, rating: int, card_id: int, token: str, deck_id: int):
        get_card = requests.get(
            url=f'{MAIN_URL_API}cards/{card_id}/',
            headers={
                'Authorization': f'Token {token}'
            }
        ).json()
        answer = GetCardAnswer.parse_obj(get_card)
        if answer.review_date:
            review = SMTwo(
                answer.easiness,
                answer.interval,
                answer.repetitions
            ).review(rating, answer.review_date)
        else:
            review = SMTwo.first_review(quality=rating)
        requests.put(
            url=f'{MAIN_URL_API}cards/{card_id}/',
            headers={
                'Authorization': f'Token {token}'
            },
            data={
                'easiness': review.easiness,
                'interval': review.interval,
                'repetitions': review.repetitions,
                'review_date': review.review_date
            }
        )
        self.study(deck_id=deck_id)
