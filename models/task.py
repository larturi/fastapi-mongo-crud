import datetime
from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    id: Optional[str]
    title: str
    is_open: bool
    created_at: datetime.datetime