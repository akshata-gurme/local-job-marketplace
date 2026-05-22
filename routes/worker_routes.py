from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
import database
import models

router = APIRouter()

@router.post("/submit_worker")
async def create_worker(
    f_name: str = Form(...),
    f_skill: str = Form(...),
    f_wage: int = Form(...),
    f_exp: int = Form(...),
    f_loc: str = Form(...),
    f_whatsapp: str = Form(...),
    db: Session = Depends(database.get_db)
):
    new_worker = models.Worker(
        full_name=f_name, 
        skill=f_skill, 
        daily_wage=f_wage,
        experience=f_exp, 
        location=f_loc, 
        whatsapp_no=f_whatsapp
    )
    db.add(new_worker)
    db.commit()
    return {"status": "Success", "message": f"Profile created for {f_name}"}