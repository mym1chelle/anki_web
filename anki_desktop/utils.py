import csv
import tkinter as tk
import customtkinter as ct
from tkinter import filedialog, messagebox
import requests
from pydantic_schemas import Decks, Styles


win_width = 700
win_height = 800

root = tk.Tk()
# root = ct.CTk()


MAIN_URL_API = 'http://127.0.0.1:8000/api/v1/'
BG_COLOR = '#323232'
TEXT_COLOR = 'white'


def search_deck(name, decks: Decks):
    return next((deck.id for deck in decks.results if deck.name == name), None)


def search_styles(name, styles: Styles):
    return next((style.id for style in styles.styles if style.name == name), None)


def take_window_of_center(win_x: int, win_y: int):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return int((screen_width / 2) - (win_x / 2)), int((screen_height / 2) - (win_y / 2))


def get_type_code(type_name: str) -> str | None:
    if type_name == 'Markdown':
        return 'md'
    elif type_name == 'Text':
        return 'text'
    elif type_name == 'HTML':
        return 'html'
    return None


def load_and_import_file(
        window: tk.Tk,
        new_window: tk.Toplevel,
        question_type_code: str,
        answer_type_code: str,
        card_style: str,
        styles: Styles,
        deck_name: str,
        decks: Decks,
        token: str,
        study
):
    deck_id = search_deck(deck_name, decks)
    style_id = search_styles(card_style, styles)
    window.filename = filedialog.askopenfilename(
        initialdir='/Users/timursamusenko/Downloads/',
        title='Выберите файл',
        filetypes=(('csv файлы', '*.csv'),))

    if window.filename:
        cards_count_in_file = len([line for line in open(file=window.filename).readline()])
        with open(file=window.filename) as file:
            read = csv.reader(file)
            yes_no = messagebox.askyesnocancel(message=f'Импортировать карточки ({cards_count_in_file})?')
            if yes_no:
                for row in read:
                    # try:
                    requests.post(
                        url=f"{MAIN_URL_API}cards/create/",
                        data={
                            "question": row[0],
                            "question_type": question_type_code,
                            "answer": row[1],
                            "answer_type": answer_type_code,
                            "style": style_id,
                            "deck": deck_id
                        },
                        headers={
                            'Authorization': f'Token {token}'
                        }
                    )
                    # except:
                    #     messagebox.showerror(message='Неудалось подключиться к серверу')
                messagebox.showinfo(message='Карточки были успешно импортированы')
        new_window.destroy()
        study.show_decks()
