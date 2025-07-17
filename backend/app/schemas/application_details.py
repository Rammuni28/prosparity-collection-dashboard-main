from pydantic import BaseModel
from typing import Optional

class ApplicationDetailsOut(BaseModel):
    id: int
    applicant_id: str
    applicant_name: str
    branch_name: Optional[str]
    team_lead: Optional[str] = None
    rm_name: Optional[str] = None
    dealer_name: Optional[str]
    lender_name: Optional[str] = None
    lms_status: Optional[str] = None
    field_status: Optional[str] = None
    emi_amount: Optional[float]
    principle_due: Optional[float]
    interest_due: Optional[float]
    demand_date: Optional[str]
    user_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    applicant_mobile: Optional[str] = None
    applicant_address: Optional[str] = None
    house_ownership: Optional[str] = None
    co_applicant_name: Optional[str] = None
    co_applicant_mobile: Optional[str] = None
    co_applicant_address: Optional[str] = None
    guarantor_name: Optional[str] = None
    guarantor_mobile: Optional[str] = None
    guarantor_address: Optional[str] = None
    reference_name: Optional[str] = None
    reference_mobile: Optional[str] = None
    reference_address: Optional[str] = None
    fi_location: Optional[str] = None
    repayment: Optional[str] = None
    last_month_bounce: Optional[int] = None
    collection_rm: Optional[str] = None
    ptp_date: Optional[str] = None
    paid_date: Optional[str] = None
    applicant_calling_status: Optional[str] = None
    co_applicant_calling_status: Optional[str] = None
    guarantor_calling_status: Optional[str] = None
    reference_calling_status: Optional[str] = None
    latest_calling_status: Optional[str] = None
    disbursement_date: Optional[str] = None
    loan_amount: Optional[float] = None
    vehicle_status: Optional[str] = None
    amount_collected: Optional[float] = None

    class Config:
        orm_mode = True 

class ApplicationDetailsCreate(BaseModel):
    # Applicant fields
    applicant_id: str
    applicant_first_name: str
    applicant_middle_name: Optional[str] = None
    applicant_last_name: Optional[str] = None
    applicant_mobile: Optional[int] = None
    applicant_address_line1: Optional[str] = None
    applicant_address_line2: Optional[str] = None
    applicant_address_line3: Optional[str] = None
    applicant_city: Optional[str] = None
    applicant_state: Optional[str] = None
    applicant_pincode: Optional[int] = None
    ownership_type_id: Optional[int] = None
    branch_id: Optional[int] = None
    dealer_id: Optional[int] = None
    fi_location: Optional[str] = None

    # Loan fields
    approved_amount: float
    disbursal_amount: float
    approved_rate: float
    disbursal_date: Optional[str] = None
    dollection_relationship_manager_id: Optional[int] = None
    source_relationship_manager_id: Optional[int] = None
    tenure: int

    # Payment fields
    demand_amount: float
    principal_amount: float
    interest: float
    demand_date: Optional[str] = None
    demand_month: Optional[int] = None
    demand_year: Optional[int] = None
    demand_num: Optional[int] = None
    amount_collected: Optional[float] = None
    fees: Optional[float] = None
    fees_status: Optional[str] = None
    payment_date: Optional[str] = None
    Repayment_status_id: Optional[int] = None
    mode: Optional[str] = None
    payment_information: Optional[str] = None 