FROM python:3.6-jessie

ENV DJANGO_SETTINGS_MODULE=podcasts.settings \
    PYTHONPATH=/home/app/code/src

COPY requirements.txt /tmp/requirements.txt

RUN rm -rf /var/cache/apt && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/cache/apt && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip==9.0.1 setuptools==34.4.1 && \
    pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

COPY . /home/app/code
WORKDIR /home/app/code

RUN django-admin collectstatic --no-input
