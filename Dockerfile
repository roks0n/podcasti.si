FROM python:3.7-stretch

ENV DJANGO_SETTINGS_MODULE=podcasts.settings \
    PYTHONPATH=/home/app/code/src

COPY requirements.txt /tmp/requirements.txt

RUN rm -rf /var/cache/apt && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/cache/apt && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip setuptools && \
    pip install pip-tools==4.2.0 && \
    pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

COPY . /home/app/code
WORKDIR /home/app/code

RUN django-admin collectstatic --no-input
