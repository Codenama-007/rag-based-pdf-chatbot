from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from dotenv import load_dotenv
import os

load_dotenv

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing 
def hash_password(password: str):
    return password_hash.hash(password)


# Verifying the Hash Password 
def verify_password(password: str, hashed: str):
    return password_hash.verify(password, hashed)


# Creating the Access token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )