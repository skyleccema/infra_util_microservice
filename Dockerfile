# syntax=docker/dockerfile:1

FROM python:3.13

RUN mkdir app infra_utils
COPY ./.env ./app
COPY ./app ./app
COPY ./infra_utils ./infra_utils
RUN pip install flask ./infra_utils/v2.0/dist/infra_utils_sqlalchemy_2.0-0.0.2-py3-none-any.whl

CMD ["flask", "run", "--host=0.0.0.0"]
