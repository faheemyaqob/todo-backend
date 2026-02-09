"""
JWT token utilities for authentication
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    exp: Optional[datetime] = None


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """JWT payload model"""
    sub: str
    exp: datetime


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing claims to encode
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        logger.info(f"JWT token created for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT token: {e}")
        raise


def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Decode and verify a JWT token
    
    Args:
        token: JWT token to decode
        
    Returns:
        TokenPayload if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        
        if username is None:
            logger.warning("Token missing 'sub' claim")
            return None
        
        exp = payload.get("exp")
        if exp is None:
            logger.warning("Token missing 'exp' claim")
            return None
        
        token_data = TokenPayload(
            sub=username,
            exp=datetime.fromtimestamp(exp, tz=timezone.utc)
        )
        return token_data
    
    except JWTError as e:
        logger.warning(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error decoding token: {e}")
        return None
