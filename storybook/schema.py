from datetime import datetime
from ninja import Schema, File
from uuid import UUID  # Import UUID
from typing import List, Optional

class StorybookSchema(Schema):
    title: str
    duration: float
    iterations: int
    status: bool

class StorybookResponseSchema(Schema):
    id: UUID
    title: str
    createdAt: datetime
    duration: float
    iterations: int
    status: bool

class ImageSchema(Schema):
    image: str
    prompt: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        
class ImageResponseSchema(Schema):
    id: UUID
    storybook_id: UUID
    image: str  
    description: str 
    class Config:
        arbitrary_types_allowed = True

class ImageGetStorybookImages(Schema):
    id: UUID
    image: File
    description: str 
    class Config:
        arbitrary_types_allowed = True

class ImageListResponseSchema(Schema):
    storybook_id: UUID
    image_list: List[ImageGetStorybookImages]
    
class DescriptionSchema(Schema):
    description: str
    
class DescriptionResponseSchema(Schema):
    id: UUID
    storybook_id: UUID
    description: str
    
class DescriptionAllSchema(Schema):
    id: UUID
    description: str

class DescriptionListResponseSchema(Schema):
    storybook_id: UUID
    description_list: List[DescriptionAllSchema]

class GenerateTextSchema(Schema):
    user_input: str

class NotFoundSchema(Schema):
    message: str
    
    