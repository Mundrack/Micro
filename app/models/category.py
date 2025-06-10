from beanie import Document
from pydantic import Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class Category(Document):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
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
        name = "categories"
        
    def __str__(self):
        return f"Category(name='{self.name}')"
        
    def __repr__(self):
        return self.__str__()