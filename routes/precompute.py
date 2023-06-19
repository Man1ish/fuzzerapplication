from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import PrecomputeSearchInput, PrecomputeSearchResponse
from utils.precompute_crud import (
    precompute_search
)

router_precompute = APIRouter(tags=["precomputes"])


@router_precompute.post("/search", status_code=status.HTTP_200_OK, response_model=PrecomputeSearchResponse)
def get_precompute_search(precompute: PrecomputeSearchInput, db: Session = Depends(get_db)):
    result, status = precompute_search(db=db,search=precompute)
    if status:
        return PrecomputeSearchResponse(
        latitude = result['latitude'],longitude = result['longitude'],name = result['name'],description = result['description'],magnitude = result['magnitude'],location=result['location'],image=result['image'],status=result['status'],id=result['id'])

    else:
        return PrecomputeSearchResponse(
            latitude=0, longitude=0, name="", description="", magnitude=0, location="", image="", status=False)