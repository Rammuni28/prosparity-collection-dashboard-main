from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.schemas.comments import (
    CommentCreate, 
    CommentUpdate, 
    CommentResponse, 
    CommentListResponse,
    CommentWithUserInfo
)
from app.crud.comments import (
    create_comment,
    get_comment,
    get_comments_by_repayment,
    get_comments_by_application,
    get_all_comments,
    update_comment,
    delete_comment,
    get_comments_count_by_repayment,
    get_comments_count_by_application
)
from app.crud.user import get_user

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

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment_by_id(
    comment_id: int = Path(..., description="The ID of the comment to retrieve"),
    db: Session = Depends(get_db)
):
    """Get a specific comment by ID"""
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.get("/repayment/{repayment_id}", response_model=CommentListResponse)
def get_comments_by_repayment_id(
    repayment_id: str = Path(..., description="The repayment ID to get comments for"),
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of comments to return"),
    db: Session = Depends(get_db)
):
    """Get all comments for a specific repayment"""
    comments = get_comments_by_repayment(db, repayment_id, skip, limit)
    total = get_comments_count_by_repayment(db, repayment_id)
    
    return CommentListResponse(total=total, results=comments)

@router.get("/application/{application_id}", response_model=CommentListResponse)
def get_comments_by_application_id(
    application_id: str = Path(..., description="The application ID to get comments for"),
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of comments to return"),
    db: Session = Depends(get_db)
):
    """Get all comments for a specific application"""
    comments = get_comments_by_application(db, application_id, skip, limit)
    total = get_comments_count_by_application(db, application_id)
    
    return CommentListResponse(total=total, results=comments)

@router.get("/", response_model=CommentListResponse)
def get_all_comments_paginated(
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of comments to return"),
    db: Session = Depends(get_db)
):
    """Get all comments with pagination"""
    comments = get_all_comments(db, skip, limit)
    # For total count, we'll need to implement a more efficient method
    # For now, using a reasonable estimate
    total = len(comments) if len(comments) < limit else limit * 10
    
    return CommentListResponse(total=total, results=comments)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_existing_comment(
    comment_id: int = Path(..., description="The ID of the comment to update"),
    comment_update: CommentUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an existing comment"""
    updated_comment = update_comment(db, comment_id, comment_update)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/{comment_id}")
def delete_existing_comment(
    comment_id: int = Path(..., description="The ID of the comment to delete"),
    db: Session = Depends(get_db)
):
    """Delete a comment"""
    success = delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return {"message": "Comment deleted successfully"}

@router.get("/repayment/{repayment_id}/count")
def get_repayment_comments_count(
    repayment_id: str = Path(..., description="The repayment ID to get comment count for"),
    db: Session = Depends(get_db)
):
    """Get the count of comments for a specific repayment"""
    count = get_comments_count_by_repayment(db, repayment_id)
    return {"repayment_id": repayment_id, "comment_count": count}

@router.get("/application/{application_id}/count")
def get_application_comments_count(
    application_id: str = Path(..., description="The application ID to get comment count for"),
    db: Session = Depends(get_db)
):
    """Get the count of comments for a specific application"""
    count = get_comments_count_by_application(db, application_id)
    return {"application_id": application_id, "comment_count": count}