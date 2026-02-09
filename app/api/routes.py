"""
API routes for Todo management and Authentication
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta
from app.models.todo import Todo, TodoCreate
from app.auth.jwt import create_access_token, Token
from app.auth.dependencies import get_current_user
from app.services.kafka_service import kafka_service

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage for todos (for demo purposes)
todos_db: dict = {}
todo_id_counter = 1

# Dummy users for demonstration (plaintext for demo/dev, NOT for production!)
# In production, always use proper password hashing
DEMO_USERS = {
    "admin": "admin123",
    "user": "user123",
    "demo": "demo123"
}


# ===================== AUTHENTICATION ROUTES =====================

@router.post("/auth/login", response_model=Token, tags=["authentication"])
async def login(username: str, password: str) -> Token:
    """
    Login endpoint - authenticate user and return JWT token
    
    For demo purposes, use one of these credentials:
    - username: "admin", password: "admin123"
    - username: "user", password: "user123"
    - username: "demo", password: "demo123"
    
    Args:
        username: Username for login
        password: Password for login
        
    Returns:
        Token object with access_token and token_type
    """
    try:
        # Check if user exists
        if username not in DEMO_USERS:
            logger.warning(f"Login attempt with non-existent user: {username}")
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        # Verify password (simple string comparison for demo users)
        stored_password = DEMO_USERS[username]
        if password != stored_password:
            logger.warning(f"Failed login attempt for user: {username}")
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        # Create JWT token
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=30)
        )
        
        logger.info(f"User logged in successfully: {username}")
        return Token(access_token=access_token, token_type="bearer")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Login error")


# ===================== TODO ROUTES (AUTH REQUIRED) =====================

@router.post("/todos", response_model=Todo, status_code=201, tags=["todos"])
async def create_todo(
    todo: TodoCreate,
    current_user: str = Depends(get_current_user)
) -> Todo:
    """
    Create a new todo (requires authentication)
    
    Args:
        todo: Todo data to create
        current_user: Authenticated user (extracted from JWT token)
        
    Returns:
        Created todo with ID and timestamps
    """
    global todo_id_counter
    
    try:
        # Generate unique ID
        new_id = todo_id_counter
        todo_id_counter += 1
        
        # Create todo object
        now = datetime.utcnow()
        new_todo = Todo(
            id=new_id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=now,
            updated_at=now
        )
        
        # Store in memory
        todos_db[new_id] = new_todo
        
        # Publish to Kafka
        todo_message = {
            "id": new_todo.id,
            "title": new_todo.title,
            "description": new_todo.description,
            "completed": new_todo.completed,
            "created_at": new_todo.created_at.isoformat(),
            "created_by": current_user,
            "event": "todo_created"
        }
        kafka_service.publish_message(todo_message)
        
        logger.info(f"Todo created with ID: {new_id} by user: {current_user}")
        return new_todo
    
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        raise HTTPException(status_code=500, detail="Error creating todo")


@router.get("/todos", response_model=List[Todo], tags=["todos"])
async def get_todos(current_user: str = Depends(get_current_user)) -> List[Todo]:
    """
    Get all todos (requires authentication)
    
    Args:
        current_user: Authenticated user (extracted from JWT token)
        
    Returns:
        List of all todos
    """
    try:
        todos = list(todos_db.values())
        logger.info(f"Retrieved {len(todos)} todos for user: {current_user}")
        return todos
    except Exception as e:
        logger.error(f"Error retrieving todos: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving todos")


@router.get("/todos/{todo_id}", response_model=Todo, tags=["todos"])
async def get_todo(
    todo_id: int,
    current_user: str = Depends(get_current_user)
) -> Todo:
    """
    Get a specific todo by ID (requires authentication)
    
    Args:
        todo_id: ID of the todo to retrieve
        current_user: Authenticated user (extracted from JWT token)
        
    Returns:
        Todo object
    """
    try:
        if todo_id not in todos_db:
            raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")
        
        logger.info(f"Retrieved todo {todo_id} for user: {current_user}")
        return todos_db[todo_id]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving todo")


@router.put("/todos/{todo_id}", response_model=Todo, tags=["todos"])
async def update_todo(
    todo_id: int,
    todo_update: TodoCreate,
    current_user: str = Depends(get_current_user)
) -> Todo:
    """
    Update a todo (requires authentication)
    
    Args:
        todo_id: ID of the todo to update
        todo_update: Updated todo data
        current_user: Authenticated user (extracted from JWT token)
        
    Returns:
        Updated todo object
    """
    try:
        if todo_id not in todos_db:
            raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")
        
        existing_todo = todos_db[todo_id]
        
        # Update fields
        existing_todo.title = todo_update.title
        existing_todo.description = todo_update.description
        existing_todo.completed = todo_update.completed
        existing_todo.updated_at = datetime.utcnow()
        
        # Publish to Kafka
        todo_message = {
            "id": existing_todo.id,
            "title": existing_todo.title,
            "description": existing_todo.description,
            "completed": existing_todo.completed,
            "updated_at": existing_todo.updated_at.isoformat(),
            "updated_by": current_user,
            "event": "todo_updated"
        }
        kafka_service.publish_message(todo_message)
        
        logger.info(f"Todo {todo_id} updated by user: {current_user}")
        return existing_todo
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating todo")


@router.delete("/todos/{todo_id}", status_code=204, tags=["todos"])
async def delete_todo(
    todo_id: int,
    current_user: str = Depends(get_current_user)
):
    """
    Delete a todo (requires authentication)
    
    Args:
        todo_id: ID of the todo to delete
        current_user: Authenticated user (extracted from JWT token)
    """
    try:
        if todo_id not in todos_db:
            raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")
        
        deleted_todo = todos_db.pop(todo_id)
        
        # Publish to Kafka
        todo_message = {
            "id": deleted_todo.id,
            "deleted_by": current_user,
            "event": "todo_deleted"
        }
        kafka_service.publish_message(todo_message)
        
        logger.info(f"Todo {todo_id} deleted by user: {current_user}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting todo")
