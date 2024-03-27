# FastAPI App with PostgreSQL and Docker

## Introduction

This is an API for the goalforge app.

## Features

- FastAPI for building API endpoints
- PostgreSQL for database storage
- Docker for containerization
- SQLAlchemy as the ORM (Object-Relational Mapping)
- Pyright for type checking

## Prerequisites

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed
- [Poetry] (<https://python-poetry.org/docs/>) installed

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/WhiskyToad/fastapi-starter
   cd fastapi-starter
   ```

2. **Configure Environment Variables:**

Copy the .env.example file in the root of the project and configure your environment variables.

3. **Install the dependancies locally:**

We use poetry to manage this project, you will want to ensure you create virtual environments locally

   ```bash
   poetry config virtualenvs.in-project true
   ```

And then run this command to install the dependancies and create a local .venv file

   ```bash
   poetry install
   ```

Make sure your ide is configured to use this .venv as your interpretor for python

4. **Build and Run the Docker Container:**

   ```bash
   docker compose up --build

   ```

5. **Access the FastAPI App:**

Open your browser and navigate to <http://localhost:8000/docs> to access the FastAPI Swagger documentation.

6. **Stop the Docker Container:**

   ```bash
   docker-compose down
   ```

## Making migrations

We use alembic for migrations, here are the commands that will need to be ran inside your docker terminal. When you make new models add them to the init file in the models folder to be picked up.

**Make migration:**

```bash
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

## Tests

Tests are all under the test folder and split into different folders within. It spins up a SQLite database for each test run and you can run the tests with the command

   ```bash
   poetry run pytest
   ```

## Types

This project is managed by pyright, you should have the pylance extension installed from vscode and can run the checker with this command

   ```bash
   poetry run pyright
   ```
