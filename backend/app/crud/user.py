from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import verify_password, get_password_hash
from typing import Optional
from datetime import datetime

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user with hashed password"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        user_name=user.email.split('@')[0],  # Use email prefix as user_name
        password=hashed_password,
        email=user.email,
        mobile=user.mobile,
        role=user.role,
        status=user.status or 'active'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
    """Update user password"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    user.updated_at = datetime.utcnow()
    db.commit()
    return True

def verify_user_password(db: Session, user_id: int, password: str) -> bool:
    """Verify user's current password"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    return verify_password(password, user.password)

def get_users_by_role(db: Session, role: str) -> list[User]:
    """Get all users by role"""
    return db.query(User).filter(User.role == role).all()

def update_user_role(db: Session, user_id: int, new_role: str) -> bool:
    """Update user role"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    user.role = new_role
    user.updated_at = datetime.utcnow()
    db.commit()
    return True

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    return True

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID (alias for get_user_by_id)"""
    return get_user_by_id(db, user_id)

# Legacy function for backward compatibility
def verify_user(db: Session, email: str, password: str) -> Optional[User]:
    """Legacy verify_user function - use authenticate_user instead"""
    return authenticate_user(db, email, password) 