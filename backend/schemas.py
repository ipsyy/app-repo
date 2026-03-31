from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    created_at:  datetime

    model_config = {"from_attributes": True}