from datetime import datetime
import os
from uuid import UUID  # Import UUID
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from ninja.errors import HttpError

from storybook.models import Storybook
from storybook.models import Image

# Django Schema related imports
from storybook.schema import StorybookSchema, StorybookResponseSchema, NotFoundSchema
from storybook.schema import ImageSchema, ImageResponseSchema, ImageListResponseSchema

# Django Image related imports
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image as PILImage


api = NinjaAPI()
# Retrieve all storybooks
@api.get("/storybooks", response=List[StorybookResponseSchema])
def storybooks(request):
    return 200, Storybook.objects.all() 

# Retrieve a storybook with a given id
@api.get("/storybooks/{storybook_id}", response={200: StorybookResponseSchema, 404: NotFoundSchema})
def storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        return storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}


# Create a new storybook
@api.post("/storybooks", response={201: StorybookResponseSchema})
def create_storybook(request, storybook: StorybookSchema):
     # Set the 'createdAt' field to the current date and time in the request data
    storybook_data = storybook.dict()
    storybook_data['createdAt'] = datetime.now()

    # Create a new storybook
    new_storybook = Storybook.objects.create(**storybook_data)

    # Return the id and other details of the newly created storybook
    return 201, new_storybook

# Edit a storybook with a given id
@api.put("/storybooks/{storybook_id}", response={200:StorybookResponseSchema, 404: NotFoundSchema})
def change_storybook(request, storybook_id: str, data: StorybookSchema):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        for attribute, value in data.dict().items():
            setattr(storybook, attribute, value)
        storybook.save()
        return 200, storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message", "Storybook does not exist"} 

# Delete a storybook with a given id  
@api.delete("/storybooks/{storybook_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        storybook.delete()
        return 200
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}

# Retrieve storybook images with a given storybook id
@api.get("/images/{storybook_id}", response={200: ImageListResponseSchema, 404: NotFoundSchema})
def get_storybook_images(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        images = Image.objects.filter(storybook_id=storybook)

        # Create a list of dictionaries with 'id' and 'image' keys
        image_data_list = [{'id': str(image.id), 'image': image.image} for image in images]

        response_data = {
        "storybook_id": str(storybook.id),  # Convert to string
        "image_list": image_data_list,
        }
        return response_data
    
    except Storybook.DoesNotExist:
        return 404, {"message": "Storybook does not exist"}
    except Image.DoesNotExist:
        return 404, {"message": "Storybook does not have any image"}

# Upload a image using the storybook id
@api.post("/images/{storybook_id}", response={201: ImageResponseSchema, 404: NotFoundSchema})
def create_storybook_image(request, storybook_id: UUID, image: UploadedFile = File(...)):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
    except Storybook.DoesNotExist:
        return 404, {'message': 'Not Found'}
    
    # Process the uploaded image if needed
    pil_image = PILImage.open(image)    
    # Save the processed image
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')
    
    # Create a new image associated with the storybook
    new_image = Image(
        storybook_id=storybook,
        image=InMemoryUploadedFile(
            buffer, None, image.name, 'image/jpeg', buffer.tell(), None
        )
    )
    new_image.save()
    
    # Return the response with the correct UUID for storybook_id
    response_data = {
        "id": str(new_image.id),
        "storybook_id": str(storybook.id),  # Convert to string
    }
    return 201, response_data

# Delete an image with a given image id
@api.delete("/images/delete/{image_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook_image(request, image_id: UUID):
    try:
        image = Image.objects.get(pk=image_id)
        # Get the file path
        file_path = image.image.path
        # Delete the database entry
        image.delete()
        # Delete the associated file
        if os.path.exists(file_path):
            os.remove(file_path)
        return 200
    except Image.DoesNotExist:
        return 404, {"message": "Image does not exist"}
    
# Update an image with a given image id
@api.put("/images/update/{image_id}", response={200: ImageResponseSchema, 404: NotFoundSchema})
def update_storybook_image(request, image_id: UUID, image: UploadedFile = File(...)):
    try:
        existing_image = Image.objects.get(pk=image_id)
        pil_image = PILImage.open(image)
        # Save the processed image
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG')

        # Update the image data in the database
        existing_image.image = InMemoryUploadedFile(
            buffer, None, image.name, 'image/jpeg', buffer.tell(), None
        )
        existing_image.save()

        # Return the response with the correct UUID for image_id
        response_data = {
            "id": str(existing_image.id),
            "storybook_id": str(existing_image.storybook_id),  # Convert to string
        }
        return 200, response_data

    except Image.DoesNotExist:
        return 404, {"message": "Image does not exist"}
    