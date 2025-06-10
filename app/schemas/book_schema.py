from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., min_length=10, max_length=17)
    published_date: datetime
    available: bool = Field(default=True)
    author_id: str  # ObjectId como string
    category_id: str  # ObjectId como string


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    published_date: Optional[datetime] = None
    available: Optional[bool] = None
    author_id: Optional[str] = None
    category_id: Optional[str] = None


class BookResponse(BaseModel):
    id: str
    title: str
    isbn: str
    published_date: datetime
    available: bool
    author_id: str
    category_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    )