FROM python:3.11-alpine3.20
LABEL maintainer="zimmad.w@gmail.com"


COPY ./requirements.dev.txt /temp/requirements.dev.txt
COPY ./requirements.txt /temp/requirements.txt
COPY ./event_nest app/event_nest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/event_nest/event_nest
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /temp/requirements.txt && \
    if [$DEV = "true"];\
        then /py/bin/pip install -r temp/requirements.dev.txt; \
    fi && \
    rm -rf /temp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

CMD ["python", "manage.py", "runserver"]
ENV PATH="/py/bin:$PATH"

USER django-user