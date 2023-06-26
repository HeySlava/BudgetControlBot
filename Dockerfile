FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

ENV PATH=/venv/bin:$PATH
RUN :\
    && python -m venv /venv \
    && pip install --no-cache-dir pip -U wheel setuptools -r requirements.txt \
    && :

COPY ./bot .

CMD ["python",  "main.py"]
