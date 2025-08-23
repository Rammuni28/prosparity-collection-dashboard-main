from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.comments import CommentCreate, CommentResponse, CommentListResponse, CommentTypeEnum
from app.crud.comments import create_comment, get_comments_by_repayment, get_comments_count_by_repayment, get_comments_by_repayment_and_type, get_comments_count_by_repayment_and_type

router = APIRouter()

@router.post("/", response_model=CommentResponse)
def create_new_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """Create a new comment"""
    try:
        return create_comment(db, comment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create comment: {str(e)}")

@router.get("/repayment/{repayment_id}", response_model=CommentListResponse)
def get_comments_by_repayment_id(
    repayment_id: str = Path(..., description="The repayment ID (payment_details.id) to get comments for"),
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of comments to return"),
    db: Session = Depends(get_db)
):
    """Get all comments for a specific repayment (payment_details.id)"""
    comments = get_comments_by_repayment(db, repayment_id, skip, limit)
    total = get_comments_count_by_repayment(db, repayment_id)
    
    return CommentListResponse(total=total, results=comments)

@router.get("/repayment/{repayment_id}/type/{comment_type}", response_model=CommentListResponse)
def get_comments_by_repayment_and_type_route(
    repayment_id: str = Path(..., description="The repayment ID (payment_details.id) to get comments for"),
    comment_type: CommentTypeEnum = Path(..., description="Comment type: 1 for application details, 2 for paid pending"),
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of comments to return"),
    db: Session = Depends(get_db)
):
    """Get comments for a specific repayment by comment type"""
    comments = get_comments_by_repayment_and_type(db, repayment_id, comment_type, skip, limit)
    total = get_comments_count_by_repayment_and_type(db, repayment_id, comment_type)
    
    return CommentListResponse(total=total, results=comments)

@router.get("/repayment/{repayment_id}/count")
def get_repayment_comments_count(
    repayment_id: str = Path(..., description="The repayment ID (payment_details.id) to get comment count for"),
    db: Session = Depends(get_db)
):
    """Get the count of all comments for a specific repayment (payment_details.id)"""
    count = get_comments_count_by_repayment(db, repayment_id)
    return {"repayment_id": repayment_id, "comment_count": count}

@router.get("/repayment/{repayment_id}/type/{comment_type}/count")
def get_repayment_comments_count_by_type(
    repayment_id: str = Path(..., description="The repayment ID (payment_details.id) to get comment count for"),
    comment_type: CommentTypeEnum = Path(..., description="Comment type: 1 for application details, 2 for paid pending"),
    db: Session = Depends(get_db)
):
    """Get the count of comments for a specific repayment by comment type"""
    count = get_comments_count_by_repayment_and_type(db, repayment_id, comment_type)
    return {"repayment_id": repayment_id, "comment_type": comment_type, "comment_count": count}