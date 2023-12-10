from datetime import datetime
from ninja import Schema
from uuid import UUID  # Import UUID
from typing import List

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
    # image: bytes
    # storybook_id: UUID
    description: str

class ImageResponseSchema(Schema):
    # image: bytes
    id: UUID
    storybook_id: UUID
    description: str
    
# Response schema for a list of images
class ImageListResponseSchema(Schema):
    # images: List[ImageSchema]
    storybook_id: UUID
    description_list: List[ImageSchema]

class NotFoundSchema(Schema):
    message: str