from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import text
from database.models import Precompute
from schemas.models import PrecomputeSearchInput


def precompute_search(db: Session, search: PrecomputeSearchInput):
    query = text(
        "SELECT name,description,latitude,longitude,magnitude,image,location,created_at,updated_at,id FROM precompute WHERE ST_DWithin(point, ST_GeomFromText('POINT(:val1 :val2)',4269), 0.005) AND magnitude = :val3")

    # bind the values to the query
    query = query.bindparams(val1=search.latitude, val2=search.longitude, val3=search.magnitude)

    # execute the query
    result = db.execute(query).first()

    if result is not None:
        data = {"name": result[0],"description":result[1],"latitude":result[2],"longitude":result[3],"magnitude":result[4],"image":result[5],"location":result[6],"status":True,"id":result[7]}
        return data, True
    else:
        return None, False
