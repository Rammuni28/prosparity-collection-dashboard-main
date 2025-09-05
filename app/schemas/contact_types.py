from enum import Enum

class ContactTypeEnum(int, Enum):
    """Contact types for calling records"""
    applicant = 1           # Main applicant
    co_applicant = 2        # Co-applicant
    guarantor = 3           # Guarantor
    reference = 4           # Reference person
