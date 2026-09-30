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

The client scoring model is currently deterministic. Machine learning is planned.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, pandas
- **Database:** PostgreSQL, Psycopg 3, async connection pooling
- **Testing:** pytest
- **Frontend:** React, Vite, Tailwind CSS *(dashboard currently being rebuilt)*

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
benchmarks/           # API performance benchmarks and analysis
data/                 # Sample logistics data
frontend/             # React dashboard
```

## Performance Benchmarks

The synchronous and asynchronous database implementations were compared using `oha`
across multiple API endpoints and concurrency levels.

The results show workload-dependent performance improvements. Async database access
improved throughput for several endpoints under concurrent load, while simpler
workloads showed little benefit or performed better synchronously.

Detailed benchmark results, throughput and p95 latency charts, and the Jupyter analysis
are available in `benchmarks/`.

## Run Locally

Configure the PostgreSQL connection in `.env`, then run:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m scripts.init_db
python run_server.py
```

On Windows, `run_server.py` uses `SelectorEventLoop` for compatibility with the
asynchronous Psycopg connection pool.

To recreate the tables and load sample data for local development:

```bash
python -m scripts.dev.reset_and_seed_db
```

> The reset script removes existing project data.