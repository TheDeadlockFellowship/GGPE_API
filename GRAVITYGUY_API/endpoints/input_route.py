from fastapi import APIRouter, HTTPException
from entities.input_entity import InputData
from daos.input_dao import InputDao
from datetime import datetime

router2 = APIRouter()

def init_routes2(dao: InputDao):

    @router2.post("/inputs/")
    async def add_input(input: InputData):
        try:
            dao.add_input(input)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "inputs added successfully"}

    @router2.delete("/inputs/")
    async def delete_inputs(player_name: str, run_start: datetime):
        try:
            dao.delete_inputs_by_run(player_name, run_start)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "inputs deleted successfully"}
