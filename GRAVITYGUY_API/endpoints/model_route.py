from fastapi import APIRouter, HTTPException
from entities.model_entity import Model
from daos.model_dao import ModelDao
from datetime import datetime

router1 = APIRouter()

def init_routes1(dao: ModelDao):

    @router1.get("/runs/{player_name}/{train_start}", response_model=Model)
    async def get_model(player_name: str, train_start: datetime):
        try:
            model = dao.get(player_name, train_start)
            if not model:
                raise HTTPException(status_code=404, detail="Model not found")
            return model
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))