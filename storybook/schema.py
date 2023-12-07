from datetime import datetime
from ninja import Schema

class StorybookSchema(Schema):
    title: str
    createdAt: datetime
    duration: float
    iterations: int
    status: bool

class NotFoundSchema(Schema):
    message: str