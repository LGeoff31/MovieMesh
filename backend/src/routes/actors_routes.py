from fastapi import APIRouter, Depends
from database import get_db
from services.actors_services import get_highest_grossing_actors as fetch_highest_grossing_actors

router = APIRouter()

@router.get("/highest-grossing")
def highest_grossing_actors(db=Depends(get_db)):
    """Return highest-grossing actors list"""
    return fetch_highest_grossing_actors(db)