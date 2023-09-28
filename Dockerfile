from python:3.11 as dependencies


ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv" \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

ENV PATH="$VENV_PATH/bin:$PATH"
WORKDIR /app

COPY poetry.lock pyproject.toml $PYSETUP_PATH/

# install additional dependencies
RUN /bin/sh -c set -ex; \
    apt-get update; \
    apt-get install --no-install-recommends -y postgresql-client; \
    rm -rf /var/lib/apt/lists/*


# install poetry and dependencies
RUN cd $PYSETUP_PATH; \
  pip install poetry==1.6.0; \
  poetry export --without-hashes --with-credentials -f requirements.txt -o requirements.txt; \
  pip install -U -r requirements.txt


# non-root user rights
RUN groupadd -r app && useradd --no-log-init -r -g app app && chown -R app /app

COPY --chown=app:app migrations /app/migrations
COPY --chown=app:app settings /app/settings
COPY --chown=app:app Makefile yoyo.ini pyproject.toml /app/

# layer with dev dependencies installed
FROM dependencies as development
USER root
RUN cd $PYSETUP_PATH; \
  poetry export --with dev --without-hashes --with-credentials -f requirements.txt -o requirements.txt; \
  pip install -U -r requirements.txt


COPY platon_service /app/platon_service
COPY tests /app/tests

FROM dependencies as production
USER app
COPY --chown=app:app platon_service /app/platon_service

EXPOSE 8000
CMD []
