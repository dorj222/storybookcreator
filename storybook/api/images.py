import os
from uuid import UUID

from ninja import Router, File
from ninja.files import UploadedFile

from storybook.models import Storybook
from storybook.models import Image
from storybook.schema import ImageResponseSchema, ImageListResponseSchema, NotFoundSchema

# Django Image related imports
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image as PILImage
from typing import Optional

# Import diffusion model
from storybook.llm_models import diffusion_model
import json

import time
from django.http import JsonResponse


# Import config file
config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

router = Router()

@router.get("/{storybook_id}", response={200: ImageListResponseSchema, 404: NotFoundSchema})
def get_storybook_images(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        images = Image.objects.filter(storybook_id=storybook)

        image_data_list = []
        for image in images:
            image_data_list.append(
                {'id': str(image.id), 
                 'image': image.image.url if image.image else None
                }
            )

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
def create_storybook_image(request, storybook_id: UUID, image: UploadedFile = File(...), 
                           prompt: Optional[str] = None,  parameters: Optional[str] = None):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
    except Storybook.DoesNotExist:
        return 404, {'message': 'Not Found'}

    if prompt is None:
        prompt = ""

    if parameters is None:
        parameters = {"strength": 0.1, "story_chapter": "chapter_2_prompt"}
    else:
        parameters = json.loads(parameters)

    pil_image = PILImage.open(image)
    pil_image = pil_image.convert("RGB").resize((512, 512))

    img2img_prompt = f"{prompt}, {config['img_enhancement_prompt']}"

    # image to image enhancement
    generated_image = diffusion_model.run(pil_image, prompt=img2img_prompt, strength = parameters["strength"])
    buf = BytesIO()
    generated_image.save(buf, format='JPEG')
    content_file = ContentFile(buf.getvalue())

    new_image = Image(
        storybook_id=storybook
    )
    new_image.image.save(f'{new_image.id}.jpg', content_file)
    new_image.save()

    response_data = {
        "id": str(new_image.id),
        "storybook_id": str(storybook.id),
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
        existing_image.save()
    
    response_data = {
        "id": str(existing_image.id),
        "storybook_id": str(existing_image.storybook_id.id),
        "image": existing_image.image.url if existing_image.image else None
    }
    return 200, response_data