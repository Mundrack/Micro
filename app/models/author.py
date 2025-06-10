from beanie import Document
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class Author(Document):
    name: str = Field(..., min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=1000)
    birth_date: Optional[datetime] = None
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
        name = "authors"
        
    def __str__(self):
        return f"Author(name='{self.name}')"
        
    def __repr__(self):
        return self.__str__()