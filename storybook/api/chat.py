# views.py
from ninja import Router, Schema
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from PIL import Image as PILImage
from typing import Optional


from storybook.schema import GenerateTextSchema, TranslateTextSchema, GenerateStorySchema
from storybook.llm_models.tiny_llama import generate_title
from storybook.llm_models.seamless import translate_text
from storybook.llm_models.blip import generate_image_description
# LLM Model BLIP for description text generation
from storybook.llm_models.blip import generate_image_caption

router = Router()
@router.post("/titles")
def generate_storybook_title(request, data: GenerateTextSchema):
    title_text = generate_title(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/translations")
def generate_translations(request, data: TranslateTextSchema):
    title_text = translate_text(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/descriptions")
def generate_descriptions(request, image: UploadedFile = File(...), prompt: Optional[str] = None,  chapter_index: Optional[str] = None):
    # image to text caption generation
    generated_description = generate_image_description(pil_image=image,prompt=prompt, chapter_index=chapter_index) 
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/captions")
def create_image_caption(request, image: UploadedFile = File(...)):
    caption = generate_image_caption(image)
    return JsonResponse({'caption': caption})