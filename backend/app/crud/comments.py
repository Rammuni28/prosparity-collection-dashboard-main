from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Dict, Any
from app.models.comments import Comments
from app.schemas.comments import CommentCreate, CommentTypeEnum

def create_comment(db: Session, comment: CommentCreate) -> Comments:
    """Create a new comment"""
    db_comment = Comments(
        repayment_id=comment.repayment_id,
        user_id=comment.user_id,
        comment=comment.comment,
        comment_type=comment.comment_type.value,  # Extract integer value from enum
        commented_at=func.now()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_repayment(db: Session, repayment_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Get all comments by repayment_id (which is payment_details.id)"""
    comments = db.query(Comments)\
        .filter(Comments.repayment_id == repayment_id)\
        .order_by(desc(Comments.commented_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # Convert SQLAlchemy models to dictionaries
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "repayment_id": comment.repayment_id,
            "user_id": comment.user_id,
            "comment": comment.comment,
            "comment_type": comment.comment_type,
            "commented_at": comment.commented_at
        })
    
    return result

def get_comments_by_repayment_and_type(db: Session, repayment_id: str, comment_type: CommentTypeEnum, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Get comments by repayment_id and specific comment type"""
    comments = db.query(Comments)\
        .filter(
            Comments.repayment_id == repayment_id,
            Comments.comment_type == comment_type.value  # Use integer value for filtering
        )\
        .order_by(desc(Comments.commented_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # Convert SQLAlchemy models to dictionaries
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "repayment_id": comment.repayment_id,
            "user_id": comment.user_id,
            "comment": comment.comment,
            "comment_type": comment.comment_type,
            "commented_at": comment.commented_at
        })
    
    return result

def get_comments_count_by_repayment(db: Session, repayment_id: str) -> int:
    """Get count of all comments for a repayment_id"""
    return db.query(Comments).filter(Comments.repayment_id == repayment_id).count()

def get_comments_count_by_repayment_and_type(db: Session, repayment_id: str, comment_type: CommentTypeEnum) -> int:
    """Get count of comments for a repayment_id by specific type"""
    return db.query(Comments).filter(
        Comments.repayment_id == repayment_id,
        Comments.comment_type == comment_type.value  # Use integer value for filtering
    ).count()