from pydantic import BaseModel
from typing import Optional

class OwnershipTypeBase(BaseModel):
    ownership_type_name: str

class OwnershipTypeCreate(OwnershipTypeBase):
    pass

class OwnershipTypeOut(OwnershipTypeBase):
    id: int

    class Config:
        orm_mode = True 