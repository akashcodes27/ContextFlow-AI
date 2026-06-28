from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.auth.jwt import decode_access_token
from app.db.session import get_db
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        # We defined sub:id while creating user. 

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    # SELECT * FROM users WHERE id = 'd3bfcf30-1793-4e87-8100-6002e56e1fe6' LIMIT 1;
    # Iterates through every user id in db and checks if it matches the user_id from the token. If a match is found, it returns the user object. If no match is found, it returns None.

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user