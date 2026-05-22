# WorkLocal Marketplace

WorkLocal Marketplace is a FastAPI job marketplace for connecting local workers and employers. It includes a Python API, SQLAlchemy models, and static HTML frontend pages for worker, employer, job, login, calculator, and best-performer flows.

## Features

- Worker and employer registration
- Login by email or phone number
- Job posting and job listing APIs
- Worker and employer listing APIs
- Static frontend served from FastAPI
- MySQL support through SQLAlchemy

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL with PyMySQL
- HTML, CSS, and JavaScript

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Configure the database.

Create a MySQL database named `worklocal_db`, then copy `.env.example` to `.env` and update `DATABASE_URL` if your local database credentials are different.

```powershell
Copy-Item .env.example .env
```

4. Run the app.

```powershell
uvicorn main:app --reload
```

5. Open the app.

Visit `http://127.0.0.1:8000`.

## API

The FastAPI docs are available at `http://127.0.0.1:8000/docs` while the server is running.
