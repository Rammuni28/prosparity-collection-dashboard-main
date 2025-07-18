from pydantic import BaseModel

class SummaryStatusResponse(BaseModel):
    total: int
    paid: int
    unpaid: int
    partially_paid: int
    cash_collected: int
    customer_deposited: int
    paid_pending_approval: int
    foreclose: int 