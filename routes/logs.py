from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import Logs
from database.connection import get_db
from schemas.models import LogResponse, logInput
from utils.log_crud import (
    log_save
)

router_logs = APIRouter(tags=["logs"])


@router_logs.post("/save-log", status_code=status.HTTP_201_CREATED, response_model=LogResponse)
def create_Log(log: logInput, db: Session = Depends(get_db)):
    log_save(db=db, log=log)


    return LogResponse(status="Ok")


