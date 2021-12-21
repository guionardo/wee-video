FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
RUN mkdir /code/.repository

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]