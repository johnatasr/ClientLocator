FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.5

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /var/www/app

# Install system dependencies
RUN apt-get update && apt-get install gcc build-essential libpq-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools

COPY ./requirements.txt /var/www/app
RUN pip install -r requirements.txt

# Clean the house
RUN apt-get purge libpq-dev -y && apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

COPY . /var/www/app

USER user

CMD ["sh","-c", \
    "sleep 4s && \
     python manage.py test locator.presenters.tests && \
     python manage.py test locator.infra.tests && \
     python manage.py test locator.domain.tests && \
     gunicorn clientlocator.wsgi --workers=5 --threads=2 --log-file - -b 0.0.0.0:8000 --reload"]