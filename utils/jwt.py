from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
SECRET_KEY = "vcjxƒxdfgjygtfuyhi658987"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP = 60 * 24 * 365
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data: dict, exp: timedelta | None = None):
    # Ensure data is a dict; if it's a Pydantic BaseModel, use .dict()
    if hasattr(data, "dict") and callable(getattr(data, "dict")):
        to_encode = data.dict()
    else:
        to_encode = data.copy()
    expire = datetime.utcnow() + (exp or timedelta(minutes=ACCESS_TOKEN_EXP))
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify(plain, hashed):
    print({"hashed": hashed})
    return pwd_context.verify(plain, hashed)

def encrypt(plain):
    return pwd_context.hash(plain)

def get_payload(token:str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])