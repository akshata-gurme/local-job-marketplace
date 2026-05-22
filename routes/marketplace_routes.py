from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
import hashlib
import hmac

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

import models
from database import get_db


router = APIRouter()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


class WorkerCreate(BaseModel):
    full_name: str
    email: str
    password: str
    skill: str
    daily_wage: int
    experience: int
    location: str
    whatsapp_no: str


class EmployerCreate(BaseModel):
    full_name: str
    email: str
    password: str
    location: str
    whatsapp_no: str
    skill_needed: str


class LoginRequest(BaseModel):
    username: str
    password: str


class JobCreate(BaseModel):
    employer_name: str
    employer_email: str
    employer_phone: str
    job_title: str
    skill_required: str
    location: str
    salary: int
    experience_required: int
    description: str


@router.get("/jobs")
def list_jobs(
    skill: str | None = Query(default=None),
    location: str | None = Query(default=None),
    employer_email: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    jobs_query = db.query(models.Job)
    if skill:
        jobs_query = jobs_query.filter(models.Job.skill_required == skill)
    if location:
        jobs_query = jobs_query.filter(models.Job.location == location)
    if employer_email:
        jobs_query = jobs_query.filter(models.Job.employer_email.ilike(employer_email))  # case insensitive
        log.info(f"Listing jobs for email={employer_email}")

    jobs = jobs_query.order_by(models.Job.id.desc()).all()
    return [
        {
            "id": job.id,
            "employer_name": job.employer_name,
            "employer_email": job.employer_email,
            "employer_phone": job.employer_phone,
            "job_title": job.job_title,
            "skill_required": job.skill_required,
            "location": job.location,
            "salary": job.salary,
            "experience_required": job.experience_required,
            "description": job.description,
        }
        for job in jobs
    ]


@router.post("/jobs")
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    # Validate input
    import re
    phone = payload.employer_phone.strip()
    if len(payload.employer_email) > 120 or '@' not in payload.employer_email:
        raise HTTPException(status_code=400, detail="Invalid employer_email")
    if len(phone) != 10 or not phone.isdigit():
        raise HTTPException(status_code=400, detail="Employer phone must be exactly 10 digits")
    if payload.salary <= 0 or payload.experience_required < 0:
        raise HTTPException(status_code=400, detail="Invalid salary or experience")
    
    # Update payload for DB
    payload.employer_phone = phone
    
    job = models.Job(
        employer_name=payload.employer_name,
        employer_email=payload.employer_email,
        employer_phone=payload.employer_phone,
        job_title=payload.job_title,
        skill_required=payload.skill_required,
        location=payload.location,
        salary=payload.salary,
        experience_required=payload.experience_required,
        description=payload.description,
    )
    db.add(job)
    try:
        db.commit()
        db.refresh(job)
        log.info(f"Job created: id={job.id}, email={job.employer_email}")
        return {"message": "Job posted successfully.", "job_id": job.id}
    except IntegrityError as e:
        db.rollback()
        log.error(f"DB error creating job: {e}")
        raise HTTPException(status_code=400, detail="Invalid job data - check email/phone format")
    except Exception as e:
        db.rollback()
        log.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail="Server error posting job")


@router.get("/workers")
def list_workers(db: Session = Depends(get_db)):
    workers = db.query(models.Worker).order_by(models.Worker.id.desc()).all()
    return [
        {
            "id": worker.id,
            "full_name": worker.full_name,
            "email": worker.email,
            "skill": worker.skill,
            "daily_wage": worker.daily_wage,
            "experience": worker.experience,
            "location": worker.location,
            "whatsapp_no": worker.whatsapp_no,
        }
        for worker in workers
    ]


@router.get("/employers")
def list_employers(db: Session = Depends(get_db)):
    employers = db.query(models.Employer).order_by(models.Employer.id.desc()).all()
    return [
        {
            "id": employer.id,
            "full_name": employer.full_name,
            "email": employer.email,
            "location": employer.location,
            "whatsapp_no": employer.whatsapp_no,
            "skill_needed": employer.skill_needed,
        }
        for employer in employers
    ]


@router.post("/workers")
def create_worker(payload: WorkerCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.Worker)
        .filter(
            or_(
                models.Worker.email == payload.email,
                models.Worker.whatsapp_no == payload.whatsapp_no,
            )
        )
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Worker already exists with this email or phone number.")

    worker = models.Worker(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        skill=payload.skill,
        daily_wage=payload.daily_wage,
        experience=payload.experience,
        location=payload.location,
        whatsapp_no=payload.whatsapp_no,
    )
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return {"message": "Worker profile created successfully.", "worker_id": worker.id}


@router.post("/employers")
def create_employer(payload: EmployerCreate, db: Session = Depends(get_db)):
    import re
    phone = payload.whatsapp_no.strip()
    if len(phone) != 10 or not phone.isdigit():
        raise HTTPException(status_code=400, detail="WhatsApp number must be exactly 10 digits")
    
    existing_user = (
        db.query(models.Employer)
        .filter(
            or_(
                models.Employer.email == payload.email,
                models.Employer.whatsapp_no == phone,
            )
        )
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Employer already exists with this email or phone number.")

    employer = models.Employer(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        location=payload.location,
        whatsapp_no=phone,
        skill_needed=payload.skill_needed,
    )
    db.add(employer)
    db.commit()
    db.refresh(employer)
    return {"message": "Employer account created successfully.", "employer_id": employer.id}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    worker = (
        db.query(models.Worker)
        .filter(
            or_(
                models.Worker.email == payload.username,
                models.Worker.whatsapp_no == payload.username,
            )
        )
        .first()
    )
    if worker and verify_password(payload.password, str(worker.password_hash)):
        return {
            "message": "Login successful.",
            "role": "worker",
            "user": {
                "id": worker.id,
                "full_name": worker.full_name,
                "skill": worker.skill,
                "location": worker.location,
            },
        }

    employer = (
        db.query(models.Employer)
        .filter(
            or_(
                models.Employer.email == payload.username,
                models.Employer.whatsapp_no == payload.username,
            )
        )
        .first()
    )
    if employer and verify_password(payload.password, str(employer.password_hash)):
        return {
            "message": "Login successful.",
            "role": "employer",
            "user": {
                "id": employer.id,
                "full_name": employer.full_name,
                "skill_needed": employer.skill_needed,
                "location": employer.location,
            },
        }

    raise HTTPException(status_code=401, detail="Invalid email/phone or password.")
