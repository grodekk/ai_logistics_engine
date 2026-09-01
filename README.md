# LOGISTICS DATA & DECISION ENGINE

A logistics decision-support application built with Python, FastAPI, PostgreSQL,
Pandas, and React.

The project is based on real transport-business workflows. It helps calculate required
route rates, evaluate clients, and analyze operating costs through a REST API and a
dashboard.

> Backend and API are implemented. The frontend dashboard is currently being updated.

## Features

- route pricing based on operating costs, planned trips, fixed costs, and profit target,
- rule-based client scoring and payment-risk analysis,
- cost, client, route-share, Pareto, and activity reports,
- PostgreSQL tables, views, and organized SQL queries,
- JSON data import for local development,
- automated tests and database smoke checks.

The client scoring model is currently deterministic. Machine learning is planned

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, pandas
- **Database:** PostgreSQL, psycopg2
- **Testing:** pytest
- **Frontend:** React, Vite, Tailwind CSS

## Structure

```text
src/
├── api/              # FastAPI routes, schemas and services
├── core/             # Configuration, exceptions, logging and paths
├── db/               # Database access and SQL loading
├── engines/          # Pricing and client-scoring logic
├── etl/              # JSON extraction and database loading
├── repositories/     # Data and analytics repositories
└── sql/              # Tables, views and queries

scripts/              # Database and smoke-test utilities
tests/                # Automated tests
data/                 # Sample logistics data
frontend/             # React dashboard
```

## Run Locally

Configure the PostgreSQL connection in `.env`, then run:

```bash
python -m venv venv
python -m pip install -r requirements.txt
python -m scripts.init_db
uvicorn src.api.main:app --reload
```

To recreate the tables and load sample data for local development:

```bash
python -m scripts.dev.reset_and_seed_db
```

> The reset script removes existing project data.
