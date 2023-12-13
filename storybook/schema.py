from datetime import datetime
from ninja import Schema, File
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
    image: File
    class Config:
        arbitrary_types_allowed = True

class ImageResponseSchema(Schema):
    id: UUID
    storybook_id: UUID

class ImageGetStorybookImages(Schema):
    id: UUID
    image: File
    class Config:
        arbitrary_types_allowed = True

class ImageListResponseSchema(Schema):
    storybook_id: UUID
    image_list: List[ImageGetStorybookImages]

class NotFoundSchema(Schema):
    message: str