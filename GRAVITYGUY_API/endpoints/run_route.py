from fastapi import APIRouter, HTTPException
from entities.run_entity import Run
from daos.runs_dao import RunDao
from datetime import datetime

router3 = APIRouter()

def init_routes3(dao: RunDao):

    @router3.post("/runs/")
    async def add_run(run: Run):
        try:
            dao.add_run(run)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Run added successfully"}

    @router3.delete("/runs/")
    async def delete_run(player_name: str, run_start: datetime):
        try:
            dao.delete_run(player_name, run_start)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "Run deleted successfully"}