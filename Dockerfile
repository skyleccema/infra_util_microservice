# syntax=docker/dockerfile:1

FROM python:3.13

RUN mkdir -p /app/infra_utils
COPY ./env /app
COPY ./app /app
COPY ./infra_utils /app/infra_utils
RUN pip install flask flask_cors python-dotenv /app/infra_utils/v2.0/dist/infra_utils_sqlalchemy_2.0-0.0.2-py3-none-any.whl
WORKDIR /app

CMD ["flask", "run", "--host=0.0.0.0"]
