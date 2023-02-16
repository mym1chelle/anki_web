import tkinter as tk
import customtkinter as ct
import requests
from requests.exceptions import ConnectionError
from tkinter import messagebox
from create_new_cards import CardsCreater
from create_new_deck import DeckCreater
from study_cards import CardsForStudy
from pydantic_schemas import Login, Registration
from utils import MAIN_URL_API, BG_COLOR, TEXT_COLOR


class LoginLogOutUser:
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
        """Рендерит форму для регистрации"""
        if self.login_frame:
            self.login_frame.destroy()
        if self.past_login_frame:
            self.past_login_frame.destroy()
        if self.registration_frame:
            self.registration_frame.destroy()
        self.registration_frame = tk.Frame(self.window)
        username_label = tk.Label(self.registration_frame, text='Логин')
        self.login = ct.CTkEntry(self.registration_frame)
        password_label = tk.Label(self.registration_frame, text='Пароль')
        self.password = ct.CTkEntry(self.registration_frame)
        registration_button = ct.CTkButton(
            self.registration_frame,
            command=self.registration,
            corner_radius=8,
            text='Зарегистрироваться',
        )

        username_label.grid(row=0, column=0)
        self.login.grid(row=1, column=0)
        password_label.grid(row=3, column=0)
        self.password.grid(row=4, column=0)
        registration_button.grid(row=6, column=0, pady=5)

        self.registration_frame.pack()

    def registration(self):
        """Валидация введенных данных и регистрация"""
        if self.login_error:
            self.login_error.grid_forget()
        if self.password_error:
            self.password_error.grid_forget()
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
                    self.login_error = tk.Label(self.registration_frame, text=user_data.username[0], fg='red')
                    self.login_error.grid(row=2, column=0)
                if user_data.password:
                    self.password_error = tk.Label(self.registration_frame, text=user_data.password[0], fg='red')
                    self.password_error.grid(row=5, column=0)
        except ConnectionError:
            messagebox.showerror(message='Ошибка подключения')

    def login_user(self):
        """Рендеринг формы входа пользователя"""
        if self.login_frame:
            self.login_frame.destroy()
        if self.past_login_frame:
            self.past_login_frame.destroy()
        if self.registration_frame:
            self.registration_frame.destroy()

        self.login_frame = tk.Frame(self.window)
        login_label = tk.Label(self.login_frame, text='Логин')
        self.login = ct.CTkEntry(self.login_frame)
        password_label = tk.Label(self.login_frame, text='Пароль')
        self.password = ct.CTkEntry(self.login_frame)
        login_button = ct.CTkButton(
            self.login_frame,
            text='Войти',
            command=self.authentication
        )

        self.login_frame.pack()
        login_label.grid(row=0, column=0)
        self.login.grid(row=1, column=0)
        password_label.grid(row=2, column=0)
        self.password.grid(row=3, column=0)
        login_button.grid(row=4, column=0, pady=5)

    def authentication(self):
        """Аутентификация пользователя при входе"""
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

                self.study = CardsForStudy(window=self.window, token=self.token)

                add_card = ct.CTkButton(
                    self.past_login_frame,
                    text='Создать карточку',
                    border_width=0,
                    bg_color=BG_COLOR,
                    fg_color=BG_COLOR,
                    hover=False,
                    text_color=TEXT_COLOR,
                    command=lambda: CardsCreater(
                        token=self.token,
                        window=self.window,
                        study=self.study
                    ).create_card()
                )
                add_card.grid(row=0, column=0)
                import_cards = ct.CTkButton(
                    self.past_login_frame,
                    text='Импортировать карточки',
                    border_width=0,
                    bg_color=BG_COLOR,
                    fg_color=BG_COLOR,
                    hover=False,
                    text_color=TEXT_COLOR,
                    command=lambda: CardsCreater(
                        token=self.token,
                        window=self.window,
                        study=self.study
                    ).import_cards()
                )
                import_cards.grid(row=0, column=1)
                create_deck = ct.CTkButton(
                    self.past_login_frame,
                    text='Создать колоду',
                    border_width=0,
                    bg_color=BG_COLOR,
                    fg_color=BG_COLOR,
                    hover=False,
                    text_color=TEXT_COLOR,
                    command=lambda: DeckCreater(
                        token=self.token,
                        window=self.window,
                        study=self.study
                    ).create_deck_form()
                )

                create_deck.grid(row=0, column=2)
                show_study_decks = ct.CTkButton(
                    self.past_login_frame,
                    text='Колоды',
                    border_width=0,
                    bg_color=BG_COLOR,
                    fg_color=BG_COLOR,
                    hover=False,
                    text_color=TEXT_COLOR,
                    command=lambda: self.study.show_decks()
                )
                show_study_decks.grid(row=0, column=3)
                self.past_login_frame.pack()
                self.study.show_decks()
            elif user_login.status_code == 400:
                messagebox.showerror(message=user_data.non_field_errors[0])
            else:
                messagebox.showerror(message='Ошибка при авторизации')
        except ConnectionError:
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
