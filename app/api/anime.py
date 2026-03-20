from fastapi import APIRouter
router = APIRouter(
    prefix="/anime",
    tags=["anime"],
    responses={404: {"description": "Not found"}}
)
