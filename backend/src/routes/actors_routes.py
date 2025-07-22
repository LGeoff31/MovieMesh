from fastapi import APIRouter, Depends
from database import get_db
from services.actors_services import (
    get_highest_grossing_actors as fetch_highest_grossing_actors,
    fetch_actors_by_name,
    get_actor_by_id,
    get_movies_by_actor,
    get_costars_by_actor
)
from models.models import ActorOut, MovieOut

router = APIRouter()

@router.get("/search", response_model=list[ActorOut])
def search_actors(q: str, db=Depends(get_db)):
    """Return actors matching search query"""
    return fetch_actors_by_name(db, q)

@router.get("/highest-grossing", response_model=list[ActorOut])
def highest_grossing_actors(db=Depends(get_db)):
    """Return highest-grossing actors list"""
    return fetch_highest_grossing_actors(db)

@router.get("/{id}/movies", response_model=list[MovieOut])
def get_movies_by_actor_endpoint(id: int, db=Depends(get_db)):
    """Return movies by actor"""
    return get_movies_by_actor(db, id)

@router.get("/{id}/costars", response_model=list[ActorOut])
def get_costars_by_actor_endpoint(id: int, db=Depends(get_db)):
    """Return costars by actor"""
    return get_costars_by_actor(db, id)

@router.get("/{id}", response_model=ActorOut)
def get_actor_endpoint(id: int, db=Depends(get_db)):
    """Return actor by id"""
    return get_actor_by_id(db, id)
