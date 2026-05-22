import hashlib
import hmac
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()
DATA_DIR = Path("data")
WORKERS_FILE = DATA_DIR / "workers.json"
EMPLOYERS_FILE = DATA_DIR / "employers.json"


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


def ensure_store() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for file_path in (WORKERS_FILE, EMPLOYERS_FILE):
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")


def read_records(file_path: Path) -> list[dict]:
    ensure_store()
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_records(file_path: Path, records: list[dict]) -> None:
    ensure_store()
    file_path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def next_id(records: list[dict]) -> int:
    return max((record["id"] for record in records), default=0) + 1


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


@router.get("/workers")
def list_workers():
    return read_records(WORKERS_FILE)


@router.get("/employers")
def list_employers():
    return read_records(EMPLOYERS_FILE)


@router.post("/workers")
def create_worker(payload: WorkerCreate):
    workers = read_records(WORKERS_FILE)
    existing_user = next(
        (
            worker
            for worker in workers
            if worker["email"] == payload.email or worker["whatsapp_no"] == payload.whatsapp_no
        ),
        None,
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Worker already exists with this email or phone number.")

    worker = {
        "id": next_id(workers),
        "full_name": payload.full_name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "skill": payload.skill,
        "daily_wage": payload.daily_wage,
        "experience": payload.experience,
        "location": payload.location,
        "whatsapp_no": payload.whatsapp_no,
    }
    workers.append(worker)
    write_records(WORKERS_FILE, workers)
    return {"message": "Worker profile created successfully.", "worker_id": worker["id"]}


@router.post("/employers")
def create_employer(payload: EmployerCreate):
    employers = read_records(EMPLOYERS_FILE)
    existing_user = next(
        (
            employer
            for employer in employers
            if employer["email"] == payload.email or employer["whatsapp_no"] == payload.whatsapp_no
        ),
        None,
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Employer already exists with this email or phone number.")

    employer = {
        "id": next_id(employers),
        "full_name": payload.full_name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "location": payload.location,
        "whatsapp_no": payload.whatsapp_no,
        "skill_needed": payload.skill_needed,
    }
    employers.append(employer)
    write_records(EMPLOYERS_FILE, employers)
    return {"message": "Employer account created successfully.", "employer_id": employer["id"]}


@router.post("/login")
def login(payload: LoginRequest):
    workers = read_records(WORKERS_FILE)
    worker = next(
        (
            record
            for record in workers
            if record["email"] == payload.username or record["whatsapp_no"] == payload.username
        ),
        None,
    )
    if worker and verify_password(payload.password, worker["password_hash"]):
        return {
            "message": "Login successful.",
            "role": "worker",
            "user": {
                "id": worker["id"],
                "full_name": worker["full_name"],
                "skill": worker["skill"],
                "location": worker["location"],
            },
        }

    employers = read_records(EMPLOYERS_FILE)
    employer = next(
        (
            record
            for record in employers
            if record["email"] == payload.username or record["whatsapp_no"] == payload.username
        ),
        None,
    )
    if employer and verify_password(payload.password, employer["password_hash"]):
        return {
            "message": "Login successful.",
            "role": "employer",
            "user": {
                "id": employer["id"],
                "full_name": employer["full_name"],
                "skill_needed": employer["skill_needed"],
                "location": employer["location"],
            },
        }

    raise HTTPException(status_code=401, detail="Invalid email/phone or password.")
