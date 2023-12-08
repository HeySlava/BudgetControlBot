FROM python:3.11-slim-bullseye

WORKDIR /app

COPY config.ini config.ini
COPY requirements.txt requirements.txt

ENV PATH=/venv/bin:$PATH
RUN :\
    && python -m venv /venv \
    && pip install --no-cache-dir pip -U wheel setuptools -r requirements.txt \
    && :

COPY ./bot ./bot

CMD ["python",  "bot/main.py"]
