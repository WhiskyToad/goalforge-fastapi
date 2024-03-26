FROM python:3
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install poetry==1.4.2

WORKDIR /app
# Copy poetry files
COPY pyproject.toml poetry.lock ./
COPY . /app
RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR
EXPOSE 8000