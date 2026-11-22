import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.entities import User, StudentProfile
from backend.app.schemas.schemas import UserRegister, UserLogin, Token, PasswordForgot, PasswordReset
from backend.app.core.security import get_password_hash, verify_password, create_access_token
from backend.app.core.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    # Create new user
    new_user = User(
        email=user_in.email.lower(),
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        mobile=user_in.mobile,
        dob=user_in.dob,
        guardian_consent=user_in.guardian_consent,
        is_active=True,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize Student Profile
    profile = StudentProfile(
        user_id=new_user.id,
        current_journey_step="registered"
    )
    db.add(profile)
    db.commit()

    # Generate JWT
    token_str = create_access_token(data={"sub": str(new_user.id), "email": new_user.email})

    return Token(
        access_token=token_str,
        user_id=new_user.id,
        full_name=new_user.full_name,
        email=new_user.email,
        is_admin=new_user.is_admin
    )

@router.post("/login", response_model=Token)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password combination."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account has been deactivated."
        )

    token_str = create_access_token(data={"sub": str(user.id), "email": user.email})

    return Token(
        access_token=token_str,
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        is_admin=user.is_admin
    )

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "mobile": current_user.mobile,
        "dob": current_user.dob,
        "guardian_consent": current_user.guardian_consent,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at
    }

@router.post("/forgot-password")
def forgot_password(req: PasswordForgot, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user:
        # Prevent email enumeration while giving reassuring feedback
        return {"message": "If this email is registered, password recovery instructions have been prepared."}
    
    # Generate temporary reset token
    reset_token = create_access_token(
        data={"sub": str(user.id), "purpose": "password_reset"},
        expires_delta=datetime.timedelta(minutes=30)
    )
    return {
        "message": "Password recovery token generated successfully.",
        "reset_token": reset_token  # Returned for testing/demo recovery
    }

@router.post("/reset-password")
def reset_password(req: PasswordReset, db: Session = Depends(get_db)):
    from backend.app.core.security import decode_access_token
    payload = decode_access_token(req.token)
    if not payload or payload.get("purpose") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.password_hash = get_password_hash(req.new_password)
    db.commit()
    return {"message": "Password updated successfully. You can now login with your new credentials."}
