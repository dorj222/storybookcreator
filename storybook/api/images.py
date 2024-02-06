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
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PILImage

# Import diffusion model
from storybook.llm_models import diffusion_model

router = Router()

@router.get("/{storybook_id}", response={200: ImageListResponseSchema, 404: NotFoundSchema})
def get_storybook_images(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        images = Image.objects.filter(storybook_id=storybook)
        image_data_list = [
            {'id': str(image.id), 
             'image': image.image.url if image.image else None, 
             'description': image.description} for image in images]
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

    # Prompt generation - insert Blip Model here
    
    pil_image = PILImage.open(image)
    prompt = generate_image_description(pil_image)  
    prompt = prompt + ", children's book illustration"
    print("Prompt: ", prompt)
    generated_image = diffusion_model.run(pil_image, prompt=prompt)

    # image to text caption generation
    image_description = generate_image_description(generated_image) 
    
    buf = BytesIO()
    generated_image.save(buf, format='JPEG')
    content_file = ContentFile(buf.getvalue())

    new_image = Image(
        storybook_id=storybook,
        description=image_description,
    )
    new_image.image.save(f'{new_image.id}.jpg', content_file)
    new_image.save()

    response_data = {
        "id": str(new_image.id),
        "storybook_id": str(storybook.id),
        "description": new_image.description,
        "image": new_image.image.url if new_image.image else None 
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
def update_storybook_image(request, image_id: UUID, image: UploadedFile = File(None)):
    try:
        existing_image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        return 404, {'message': 'Image Not Found'}
    
    if image:
        pil_image = PILImage.open(image)    
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG')
        existing_image.image = InMemoryUploadedFile(
            buffer, 
            None, 
            image.name, 
            'image/jpeg',
            buffer.tell(), 
            None
        )
        image_description = generate_image_description(pil_image) 
        existing_image.description = image_description

    existing_image.save()
    
    response_data = {
        "id": str(existing_image.id),
        "storybook_id": str(existing_image.storybook_id.id),
        "description": existing_image.description,
        "image": existing_image.image.url if existing_image.image else None
    }
    return 200, response_data