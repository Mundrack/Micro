from beanie import Document
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class Book(Document):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., min_length=10, max_length=17)
    published_date: datetime
    available: bool = Field(default=True)
    author_id: ObjectId
    category_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    )
    
    class Settings:
        name = "books"
        
    def __str__(self):
        return f"Book(title='{self.title}', isbn='{self.isbn}')"
        
    def __repr__(self):
        return self.__str__()