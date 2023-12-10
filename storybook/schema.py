from datetime import datetime
from ninja import Schema
from uuid import UUID  # Import UUID

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

class NotFoundSchema(Schema):
    message: str