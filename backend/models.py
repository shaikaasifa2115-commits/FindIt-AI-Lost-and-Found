from pydantic import BaseModel
from typing import Optional


class LostItem(BaseModel):
    item_name: str
    description: str
    location: str
    date: str
    contact: str
    image_url: Optional[str] = None


class FoundItem(BaseModel):
    item_name: str
    description: str
    location: str
    date: str
    contact: str
    image_url: Optional[str] = None