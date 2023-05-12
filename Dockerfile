FROM python:3.10-bullseye
MAINTAINER saeram00

WORKDIR /code

COPY ./data /code/data
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -U -r /code/requirements.txt

COPY ./main.py /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]