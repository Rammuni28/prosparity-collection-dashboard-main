from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.models.comments import Comments
from app.models.user import User
from app.schemas.comments import CommentCreate, CommentUpdate

def create_comment(db: Session, comment: CommentCreate) -> Comments:
    db_comment = Comments(
        repayment_id=comment.repayment_id,
        user_id=comment.user_id,
        comment=comment.comment,
        commented_at=comment.commented_at or func.now()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int) -> Optional[Comments]:
    return db.query(Comments).filter(Comments.id == comment_id).first()

def get_comments_by_repayment(db: Session, repayment_id: str, skip: int = 0, limit: int = 100) -> List[Comments]:
    return db.query(Comments)\
        .filter(Comments.repayment_id == repayment_id)\
        .order_by(desc(Comments.commented_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_comments_by_application(db: Session, application_id: str, skip: int = 0, limit: int = 100) -> List[Comments]:
    # Join with payment_details to get comments by application
    from app.models.payment_details import PaymentDetails
    
    return db.query(Comments)\
        .join(PaymentDetails, Comments.repayment_id == PaymentDetails.id)\
        .filter(PaymentDetails.loan_application_id == application_id)\
        .order_by(desc(Comments.commented_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_all_comments(db: Session, skip: int = 0, limit: int = 100) -> List[Comments]:
    return db.query(Comments)\
        .order_by(desc(Comments.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate) -> Optional[Comments]:
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        return None
    
    update_data = comment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int) -> bool:
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        return False
    
    db.delete(db_comment)
    db.commit()
    return True

def get_comments_count_by_repayment(db: Session, repayment_id: str) -> int:
    return db.query(Comments).filter(Comments.repayment_id == repayment_id).count()

def get_comments_count_by_application(db: Session, application_id: str) -> int:
    from app.models.payment_details import PaymentDetails
    
    return db.query(Comments)\
        .join(PaymentDetails, Comments.repayment_id == PaymentDetails.id)\
        .filter(PaymentDetails.loan_application_id == application_id)\
        .count()