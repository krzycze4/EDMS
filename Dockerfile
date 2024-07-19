FROM python:3.10
RUN apt-get update \
    && apt-get install -y curl
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root
COPY ./EDMS .
COPY EDMS/entrypoint.sh app/entrypoint.sh
RUN chmod +x app/entrypoint.sh
