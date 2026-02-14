from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import Base, SessionLocal, engine
from utils.jwt import create_token, encrypt, get_payload, oath2_schema, verify
from utils.models import LoginBase, User, UserBase
Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix="/users",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def entry():
    return({"message": "Users API"})

@router.post("/create")
def create_user(user:UserBase, db: Session = Depends(get_db)):
    hashed = encrypt(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user:LoginBase, db:Session = Depends(get_db)):
    user_query = db.query(User).filter(User.email == user.email).first()
    if user_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if verify(user.password, user_query.hashed) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    
    token = create_token(data={
        "sub": user.email
    }, exp=timedelta(minutes=30))
    return {token}

def info(token:str = Depends(oath2_schema), db:Session = Depends(get_db)):
    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="couldn't validate you"
    )
    try:
        payload = get_payload(token)
        email = payload.get("sub")
        if email is None:
            raise err
    except:
        raise err
    
    user_query = db.query(User).filter(User.email == email).first()
    if user_query is None:
        raise err
    return user_query

@router.get("/me")
def me(current_user: dict = Depends(info)):
    return {"user": current_user}
