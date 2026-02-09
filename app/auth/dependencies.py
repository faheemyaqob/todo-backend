"""
Authentication dependencies for FastAPI
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.auth.jwt import decode_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(credentials = Depends(security)) -> str:
    """
    Dependency to extract and verify JWT token from request
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        Username from decoded token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    # Decode and verify token
    token_data = decode_token(token)
    
    if token_data is None:
        logger.warning("Invalid or expired token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = token_data.sub
    if username is None:
        logger.warning("Token claims missing username")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User authenticated: {username}")
    return username
