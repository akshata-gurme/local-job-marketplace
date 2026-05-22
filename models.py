from sqlalchemy import Column, Integer, String

from database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    skill = Column(String(50), nullable=False, index=True)
    daily_wage = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    location = Column(String(50), nullable=False, index=True)
    whatsapp_no = Column(String(15), unique=True, nullable=False)


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    location = Column(String(50), nullable=False, index=True)
    whatsapp_no = Column(String(15), unique=True, nullable=False)
    skill_needed = Column(String(50), nullable=False, index=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employer_name = Column(String(100), nullable=False)
    employer_email = Column(String(120), nullable=False, index=True)
    employer_phone = Column(String(15), nullable=False)
    job_title = Column(String(120), nullable=False)
    skill_required = Column(String(50), nullable=False, index=True)
    location = Column(String(50), nullable=False, index=True)
    salary = Column(Integer, nullable=False)
    experience_required = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)

class BestPerformer(Base):
    __tablename__ = "best_performers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_name = Column(String(100), nullable=False)
    skill = Column(String(50), nullable=False)
    votes = Column(Integer, default=0)
    week = Column(String(10), default="current")

    employer_email = Column(String(120), nullable=False, index=True)
    employer_phone = Column(String(15), nullable=False)
    job_title = Column(String(120), nullable=False)
    skill_required = Column(String(50), nullable=False, index=True)
    location = Column(String(50), nullable=False, index=True)
    salary = Column(Integer, nullable=False)
    experience_required = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)
