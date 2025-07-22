from fastapi import APIRouter, Depends
from database import get_db
from services.directors_services import get_top_directors
from models.models import DirectorOut

router = APIRouter()

@router.get("/top", response_model=list[DirectorOut])
def get_top_directors_endpoint(db=Depends(get_db)):
    return get_top_directors(db)