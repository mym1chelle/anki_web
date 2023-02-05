import tkinter as tk
import requests
from tkinter import messagebox
from create_new_cards import CardsCreater
from create_new_deck import DeckCreater
from study_cards import CardsForStudy


class LoginLogOutUser:
    """
    Класс который сначала выводит на главном окне поля для логина и пароля.
    После успешной аутентификации удаляет эти поля и отображает панель для добавления карточек
    и для обучения
    """
    def __init__(self, window: tk.Tk, menu: tk.Menu):
        self.window = window
        self.menu = menu

        self.token: str = ''

        self.past_login_frame: tk.Frame = None
        self.login_frame: tk.Frame = None
        self.registration_frame: tk.Frame = None

        self.login: tk.Entry = None
        self.password: tk.Entry = None

        self.login_error: tk.Label = None
        self.password_error: tk.Label = None

        self.study = ''

    def registration_form(self):
        if self.login_frame:
            self.login_frame.destroy()
        if self.past_login_frame:
            self.past_login_frame.destroy()
        if self.registration_frame:
            self.registration_frame.destroy()
        self.registration_frame = tk.Frame(self.window)
        username_label = tk.Label(self.registration_frame, text='Логин')
        self.login = tk.Entry(self.registration_frame)
        password_label = tk.Label(self.registration_frame, text='Пароль')
        self.password = tk.Entry(self.registration_frame)
        registration_button = tk.Button(
            self.registration_frame,
            text='Зарегистрироваться',
            command=self.registration
        )

        username_label.pack()
        self.login.pack()
        password_label.pack()
        self.password.pack()
        registration_button.pack(pady=5)

        self.registration_frame.pack()

    def registration(self):
        if self.login_error:
            self.login_error.pack_forget()
        if self.password_error:
            self.password_error.pack_forget()
        get_username = self.login.get()
        get_password = self.password.get()
        try:
            registration = requests.post(
                "http://127.0.0.1:8000/api/v1/auth-token/users/",
                data={
                    "username": get_username,
                    "password": get_password,
                }
            )
            if registration.status_code == 201:
                messagebox.showinfo(message='Вы были успешно зарегестрированы')
                self.registration_frame.destroy()
                self.login_user()
            else:
                for key, value in registration.json().items():

                    if key == 'username':
                        error_text = f"Логин: {value[0]}"
                        self.login_error = tk.Label(self.registration_frame, text=error_text, fg='red')
                        self.login_error.pack()
                    else:
                        error_text = f"Пароль: {value[0]}"
                        self.password_error = tk.Label(self.registration_frame, text=error_text, fg='red')
                        self.password_error.pack()
        except:
            messagebox.showerror(message='Ошибка подключения')

    def login_user(self):
        if self.login_frame:
            self.login_frame.destroy()
        if self.past_login_frame:
            self.past_login_frame.destroy()
        if self.registration_frame:
            self.registration_frame.destroy()

        self.login_frame = tk.Frame(self.window)
        login_label = tk.Label(self.login_frame, text='Логин')
        self.login = tk.Entry(self.login_frame)
        password_label = tk.Label(self.login_frame, text='Пароль')
        self.password = tk.Entry(self.login_frame)
        login_button = tk.Button(
            self.login_frame,
            text='Войти',
            command=self.authentication
        )

        self.login_frame.pack()
        login_label.pack()
        self.login.pack()
        password_label.pack()
        self.password.pack()
        login_button.pack()

    def authentication(self):
        username = self.login.get()
        get_password = self.password.get()
        try:
            user_login = requests.post(
                url="http://127.0.0.1:8000/api/v1/auth/token/login",
                data={
                    "username": username,
                    "password": get_password
                }
            )
            if user_login.status_code == 200:
                self.menu.entryconfig('Log In', state='disabled')
                self.menu.entryconfig('Registration', state='disabled')
                self.menu.entryconfig('Log Out', state='normal')
                # убираю ненужные элементы аутентификации
                self.login_frame.destroy()
                self.token = user_login.json()['auth_token']
                # user_info = requests.get(
                #     url="http://127.0.0.1:8000/api/v1/auth-token/users/me/",
                #     headers={
                #         'Authorization': f'Token {self.token}'
                #     }
                # ).json()
                # self.user_id = user_info['id']
                self.past_login_frame = tk.LabelFrame(self.window)
            else:
                messagebox.showerror(message=user_login.json().get('non_field_errors')[0])
        except:
            messagebox.showerror(message='Ошибка подключения. Повторите попытку позже')
        add_card = tk.Button(
            self.past_login_frame,
            text='Создать карточку',
            command=lambda: CardsCreater(
                token=self.token,
                window=self.window
            ).create_card()
        )
        add_card.grid(row=0, column=0)
        import_cards = tk.Button(
            self.past_login_frame,
            text='Импортировать карточки',
            command=lambda: CardsCreater(
                token=self.token,
                window=self.window
            ).import_cards()
        )
        import_cards.grid(row=0, column=1)
        create_deck = tk.Button(
            self.past_login_frame,
            text='Создать колоду',
            command=lambda: DeckCreater(
                token=self.token,
                window=self.window
            ).create_deck_form()
        )

        self.study = CardsForStudy(window=self.window, token=self.token)

        create_deck.grid(row=0, column=2)
        show_study_decks = tk.Button(
            self.past_login_frame,
            text='Колоды',
            command=lambda: self.study.show_decks()
        )
        show_study_decks.grid(row=0, column=3)
        self.past_login_frame.pack()
        self.study.show_decks()

    def logout(self):
        create = requests.post(
            url="http://127.0.0.1:8000/api/v1/auth/token/logout",
            headers={
                'Authorization': f'Token {self.token}'
            }
        )
        if create.status_code == 204:
            self.study.hidden_decks_and_cards()
            self.menu.entryconfig('Log In', state="normal")
            self.menu.entryconfig('Registration', state="normal")
            self.menu.entryconfig('Log Out', state='disabled')
            self.past_login_frame.pack_forget()
            self.login_user()
