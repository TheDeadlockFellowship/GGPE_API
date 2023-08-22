from pydantic import BaseModel
from datetime import datetime

class Model(BaseModel):
    player_name : str
    train_start : datetime
    train_end : datetime
    parameters : bytes
