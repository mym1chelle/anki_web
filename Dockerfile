FROM python:3.11.0

COPY . /.
WORKDIR /.
EXPOSE 8000

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install