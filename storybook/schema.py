from datetime import datetime
from ninja import Schema, File
from uuid import UUID  # Import UUID
from typing import List, Optional

class StorybookSchema(Schema):
    title: str
    starting_sentence: str
    finished_playthrough: bool
    drawing: dict
    signed_the_book: bool
    decision_of_authorship: str

class StorybookResponseSchema(Schema):
    id: UUID
    title: str
    createdAt: datetime
    starting_sentence: str
    finished_playthrough: bool
    drawing: dict
    signed_the_book: bool
    decision_of_authorship: str

class ImageSchema(Schema):
    image: str
    prompt: Optional[str]
    parameters: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        
class ImageResponseSchema(Schema):
    id: UUID
    storybook_id: UUID
    image: str  
    class Config:
        arbitrary_types_allowed = True

class ImageGetStorybookImages(Schema):
    id: UUID
    image: File
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
    image_id: UUID 
    description: str
    
class DescriptionAllSchema(Schema):
    id: UUID
    image_id: UUID
    description: str

class DescriptionListResponseSchema(Schema):
    storybook_id: UUID
    description_list: List[DescriptionAllSchema]

class GenerateTextSchema(Schema):
    user_input: str

class GenerateStorySchema(Schema):
    prompt: str
    caption: str
    chapter: int

class TranslateTextSchema(Schema):
    tgt_lang: str
    user_input: str
    
class NotFoundSchema(Schema):
    message: str
    
    