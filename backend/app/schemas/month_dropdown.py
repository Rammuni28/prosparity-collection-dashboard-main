from pydantic import BaseModel
from typing import List, Optional

class MonthOption(BaseModel):
    month: str  # Format: "Aug-25"
    repayment_id: str  # The payment details ID for this month
    demand_date: str  # Full date in YYYY-MM-DD format
    is_current: bool = False  # Whether this is the current month

class MonthDropdownResponse(BaseModel):
    loan_id: str
    total_months: int
    current_month: str  # Current selected month
    months: List[MonthOption]
    message: str
