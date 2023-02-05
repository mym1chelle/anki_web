import tkinter as tk
import requests
from supermemo2 import SMTwo
from tkhtmlview import HTMLLabel


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
            url='http://127.0.0.1:8000/api/v1/study/',
            headers={
                'Authorization': f'Token {self.token}'
            }
        )
        self.show_study_decks_frame = tk.Frame(self.window)
        for num, deck in enumerate(study.json()):
            deck_name_lable = tk.Label(
                self.show_study_decks_frame,
                text='Колода'
            )
            count_new_card = tk.Label(
                self.show_study_decks_frame,
                text='Новые'
            )
            count_old_card = tk.Label(
                self.show_study_decks_frame,
                text='Повтор'
            )
            lesson = tk.Button(
                self.show_study_decks_frame,
                text=deck['name'],
                command=lambda x=deck['id']: self.study(deck_id=x)
            )
            deck_name_lable.grid(row=0, column=0)
            count_new_card.grid(row=0, column=1)
            count_old_card.grid(row=0, column=2)

            lesson.grid(row=num+1, column=0)
            new = tk.Label(self.show_study_decks_frame, text=deck['new_cards'])
            new.grid(row=num+1, column=1)
            old = tk.Label(self.show_study_decks_frame, text=deck['old_cards'])
            old.grid(row=num+1, column=2)

            self.show_study_decks_frame.pack()

    def study(self, deck_id):
        self.hidden_decks_and_cards()
        self.study_card_frame = tk.Frame(self.window)
        get_today_card = requests.get(
            url=f"http://127.0.0.1:8000/api/v1/deck/{deck_id}/cards",
            headers={
                'Authorization': f'Token {self.token}'
            }
        ).json()
        if get_today_card['results']:
            for card in get_today_card['results']:
                count = get_today_card['count']
                cards_count = tk.Label(self.study_card_frame, text=f'Осталось: {count}')
                cards_count.grid(row=1, column=0, columnspan=5)
                card_question = tk.Label(self.study_card_frame, text=card['question'])
                card_question.grid(row=2, column=0, columnspan=5)
                self.show_answer_button = tk.Button(
                    self.study_card_frame,
                    text='Ответ',
                    command=lambda: self.show_answer(answer=card['answer'], card_id=card['id'], deck_id=deck_id)
                    )
                self.show_answer_button.grid(row=3, column=0, columnspan=5)
                self.study_card_frame.pack()
        else:
            no_cards = tk.Label(self.study_card_frame, text='На сегодня все')
            no_cards.grid(row=1, column=0, columnspan=5)
            self.study_card_frame.pack()

    def show_answer(self, answer, card_id, deck_id):
        self.show_answer_button.grid_forget()
        take_answer = HTMLLabel(self.study_card_frame, html=f"<p>{answer}</p>")
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
        take_answer.grid(row=3, column=0, columnspan=5)
        button_one.grid(row=4, column=0)
        button_two.grid(row=4, column=1)
        button_three.grid(row=4, column=2)
        button_four.grid(row=4, column=3)
        button_five.grid(row=4, column=4)

    def change_card(self, rating, card_id, token, deck_id):
        get_card = requests.get(
            url=f'http://127.0.0.1:8000/api/v1/cards/{card_id}/',
            headers={
                'Authorization': f'Token {token}'
            }
        ).json()
        if get_card['review_date']:
            review = SMTwo(
                get_card['easiness'],
                get_card['interval'],
                get_card['repetitions']
            ).review(rating, get_card['review_date'])
        else:
            review = SMTwo.first_review(quality=rating)
        requests.put(
            url=f'http://127.0.0.1:8000/api/v1/cards/{card_id}/',
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
