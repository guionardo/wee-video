FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY main.py /code
RUN mkdir /code/.repository

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]