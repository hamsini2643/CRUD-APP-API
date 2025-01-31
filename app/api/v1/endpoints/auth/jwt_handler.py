import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv
import os
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
#SECRET_KEY = "nRdyqVvX1CXKT0DPuKGxqRctNv5Q3Y0tGo82jYRbxofW5LkV03AcQ20"  # Replace with a secure key
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
