FROM python:3.11.1

COPY anki_web /anki_web
COPY static /static
COPY manage.py /.
COPY pyproject.toml /.
COPY poetry.lock /.
COPY README.md /.

WORKDIR /.
EXPOSE 8000

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install