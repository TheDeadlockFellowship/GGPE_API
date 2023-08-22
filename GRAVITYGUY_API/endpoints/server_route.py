from fastapi import APIRouter
from config import SERVER

router4 = APIRouter()

@router4.get("/version")
def get_version():
    return {"version":  SERVER['version']} # Replace this with your actual versioning scheme
