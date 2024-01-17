import os
from uuid import UUID

from ninja import Router, File
from ninja.files import UploadedFile

from storybook.models import Storybook
from storybook.models import Image
from storybook.schema import ImageResponseSchema, ImageListResponseSchema, NotFoundSchema

# LLM Model BLIP for description text generation
from storybook.llm_models.blip import generate_image_description

# Django Image related imports
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image as PILImage

router = Router()

@router.get("/{storybook_id}", response={200: ImageListResponseSchema, 404: NotFoundSchema})
def get_storybook_images(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        images = Image.objects.filter(storybook_id=storybook)
        image_data_list = [{'id': str(image.id), 'image': image.image} for image in images]
        response_data = {
            "storybook_id": str(storybook.id),
            "image_list": image_data_list,
        }
        return response_data
    
    except Storybook.DoesNotExist:
        return 404, {"message": "Storybook does not exist"}
    except Image.DoesNotExist:
        return 404, {"message": "Storybook does not have any image"}

@router.post("/{storybook_id}", response={201: ImageResponseSchema, 404: NotFoundSchema})
def create_storybook_image(request, storybook_id: UUID, image: UploadedFile = File(...)):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
    except Storybook.DoesNotExist:
        return 404, {'message': 'Not Found'}

    pil_image = PILImage.open(image)
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')

    new_image = Image(
        storybook_id=storybook,
        image=InMemoryUploadedFile(
            buffer, 
            None, 
            image.name, 
            'image/jpeg',
            buffer.tell(), 
            None
        )
    )
    new_image.save()  
    pil_image = PILImage.open(buffer)
    # image to text caption generation
    image_description = generate_image_description(pil_image)  
    response_data = {
        "id": str(new_image.id),
        "storybook_id": str(storybook.id),
        "description": image_description  # Add the image_description to Response
    }
    return 201, response_data

@router.delete("/delete/{image_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook_image(request, image_id: UUID):
    try:
        image = Image.objects.get(pk=image_id)
        file_path = image.image.path
        image.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
        return 200
    except Image.DoesNotExist:
        return 404, {"message": "Image does not exist"}

@router.put("/update/{image_id}", response={200: ImageResponseSchema, 404: NotFoundSchema})
def update_storybook_image(request, image_id: UUID, image: UploadedFile = File(...)):
    try:
        existing_image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        return 404, {'message': 'Image Not Found'}
    pil_image = PILImage.open(image)    
    buffer = BytesIO()
    pil_image.save(buffer, format='JPEG')
    existing_image