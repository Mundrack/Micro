from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=1000)
    birth_date: Optional[datetime] = None


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=1000)
    birth_date: Optional[datetime] = None


class AuthorResponse(BaseModel):
    id: str
    name: str
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
    )