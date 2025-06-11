# syntax=docker/dockerfile:1

FROM python:3.13

RUN pip install flask

COPY ./app .

CMD ["flask", "run", "--host=0.0.0.0"]
