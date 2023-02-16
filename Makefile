dev:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

run:
	poetry run python anki_desktop/main.py

create:
	poetry run pyinstaller --name 'Anki' --windowed --onefile --add-data "/Users/timursamusenko/Desktop/anki_web/.venv/lib/python3.11/site-packages/customtkinter:customtkinter/"  anki_desktop/main.py