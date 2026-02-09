"""
Todo data model
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """Base Todo model with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: bool = Field(False, description="Whether the todo is completed")


class TodoCreate(TodoBase):
    """Todo model for creating a new todo"""
    pass


class Todo(TodoBase):
    """Complete Todo model with additional fields"""
    id: int = Field(..., description="Unique todo identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        from_attributes = True
