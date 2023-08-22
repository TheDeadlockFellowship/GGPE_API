from pydantic import BaseModel
from datetime import datetime

class Run(BaseModel):
    player_name: str
    run_start: datetime
    run_end: datetime
    score: int
    seed : int