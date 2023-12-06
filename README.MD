# FastAPI App with PostgreSQL and Docker

## Introduction

This is a template for a FastAPI application integrated with PostgreSQL, packaged as a Docker container. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- FastAPI for building API endpoints
- PostgreSQL for database storage
- Docker for containerization
- SQLAlchemy as the ORM (Object-Relational Mapping)
- Complete authorization operations
- Test setup

## Prerequisites

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/WhiskyToad/fastapi-starter
   cd fastapi-starter
   ```

2. **Configure Environment Variables:**

Copy the .env.example file in the root of the project and configure your environment variables.

3. **Build and Run the Docker Container:**

   ```bash
   docker compose up --build

   ```

4. **Access the FastAPI App:**

Open your browser and navigate to <http://localhost:8000/docs> to access the FastAPI Swagger documentation.

5. **Stop the Docker Container:**

   ```bash
   docker-compose down
   ```

## Making migrations

We use alembic for migrations, here are the commands that will need to be ran inside your docker terminal. When you make new models add them to the init file in the models folder to be picked up.

**Make migration:**

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Tests

Tests are all under the test folder and split into different folders within. It spins up a SQLite database for each test run and you can run the tests with the command

```bash
pytest
```
