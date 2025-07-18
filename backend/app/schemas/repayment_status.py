from pydantic import BaseModel

class RepaymentStatusOut(BaseModel):
    id: int
    repayment_status: str

    class Config:
        orm_mode = True 