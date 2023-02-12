import tkinter as tk
import requests
from tkinter import messagebox
from create_new_cards import CardsCreater
from create_new_deck import DeckCreater
from study_cards import CardsForStudy
from pydantic_schemas import Login, Registration
from utils import MAIN_URL_API


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
                f"{MAIN_URL_API}auth-token/users/",
                data={
                    "username": get_username,
                    "password": get_password,
                }
            )
            user_data = Registration.parse_obj(registration.json())
            if registration.status_code == 201:
                messagebox.showinfo(message=f'Пользователь {user_data.username} был успешно зарегестрирован')
                self.registration_frame.destroy()
                self.login_user()
            else:
                if user_data.username:
                    error_text = f"Логин: {user_data.username[0]}"
                    self.login_error = tk.Label(self.registration_frame, text=error_text, fg='red')
                    self.login_error.pack()
                if user_data.password:
                    error_text = f"Пароль: {user_data.password[0]}"
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
                url=f"{MAIN_URL_API}auth/token/login",
                data={
                    "username": username,
                    "password": get_password
                }
            )
            user_data = Login.parse_obj(user_login.json())
            if user_login.status_code == 200:
                self.menu.entryconfig('Log In', state='disabled')
                self.menu.entryconfig('Registration', state='disabled')
                self.menu.entryconfig('Log Out', state='normal')

                # убираю ненужные элементы аутентификации
                self.login_frame.destroy()
                self.token = user_data.auth_token
                self.past_login_frame = tk.LabelFrame(self.window)
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
            else:
                messagebox.showerror(message=user_data.non_field_errors[0])
        except:
            messagebox.showerror(message='Ошибка подключения. Повторите попытку позже')

    def logout(self):
        create = requests.post(
            url=f"{MAIN_URL_API}auth/token/logout",
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
