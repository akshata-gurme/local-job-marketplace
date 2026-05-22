# WorkLocal Marketplace

WorkLocal Marketplace is a local job marketplace built to help workers and employers connect quickly in one place. Workers can create profiles with their skills, wages, experience, and location, while employers can register, post jobs, and find suitable workers for local work opportunities.

The project combines a FastAPI backend, SQLAlchemy database models, and static frontend pages to create a simple full-stack marketplace experience. It is designed as a practical platform for local hiring, especially for daily-wage, skill-based, and location-based work.

## About

Finding trusted local work is often scattered across phone calls, messages, and informal contacts. WorkLocal Marketplace brings that flow into a single web application where workers can present their skills and employers can post clear job requirements.

This project focuses on real marketplace basics:

- Workers can register with their skill, daily wage, experience, location, and WhatsApp number.
- Employers can create accounts and post jobs with salary, required skill, location, and experience needs.
- Users can log in using email or phone number.
- Job listings and worker profiles can be viewed through API-backed frontend pages.
- The backend automatically creates database tables when the app starts.

It is a good portfolio project for demonstrating backend API design, database modeling, form-based frontend flows, and full-stack integration with Python and FastAPI.

## Features

- Worker and employer registration
- Login by email or phone number
- Job posting and job listing APIs
- Worker and employer listing APIs
- Best-performer and calculator frontend pages
- Static frontend served from FastAPI
- MySQL support through SQLAlchemy

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL with PyMySQL
- HTML, CSS, and JavaScript

## Project Structure

```text
.
|-- main.py                 # FastAPI app entry point
|-- database.py             # Database connection and session setup
|-- models.py               # SQLAlchemy models
|-- routes/                 # API route modules
|-- frontend/               # Static HTML frontend pages
|-- schemas/                # Extra frontend/schema files
|-- requirements.txt        # Python dependencies
`-- README.md               # Project documentation
```

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
