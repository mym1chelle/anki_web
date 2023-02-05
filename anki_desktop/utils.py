import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
root = tk.Tk()


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
        card_style_id: int,
        deck_id: int,
        token: str
):
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
                    try:
                        requests.post(
                            url="http://127.0.0.1:8000/api/v1/cards/create/",
                            data={
                                "question": row[0],
                                "question_type": question_type_code,
                                "answer": row[1],
                                "answer_type": answer_type_code,
                                "style": card_style_id,
                                "deck": deck_id
                            },
                            headers={
                                'Authorization': f'Token {token}'
                            }
                        )
                    except:
                        messagebox.showerror(message='Неудалось подключиться к серверу')
                messagebox.showinfo(message='Карточки были успешно импортированы')
        new_window.destroy()


class WrapperMap:
    """Класса для """
    def __init__(self, d: dict):
        self.d = d

    def get_value(self):
        return self.d

    def __getattr__(self, item: str):
        value = self.d.get(item)
        if isinstance(value, dict):
            return self.__class__(value)
        return value

    def __repr__(self):
        return repr(self.d)
