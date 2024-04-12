# views.py
from ninja import Router
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from typing import Optional

from storybook.schema import GenerateTextSchema, TranslateTextSchema, GenerateStorySchema
from storybook.llm_models.tiny_llama import generate_title
from storybook.llm_models.seamless import translate_text
from storybook.llm_models.blip import generate_image_description
# LLM Model BLIP for description text generation
#from storybook.llm_models.blip import generate_image_caption, generate_initial_text
from storybook.llm_models.blip_instruct import complete_sentence, continue_story, image_caption

router = Router()
@router.post("/titles")
def generate_storybook_title(request, data: GenerateTextSchema):
    title_text = generate_title(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/translations")
def generate_translations(request, data: TranslateTextSchema):
    title_text = translate_text(data.user_input, data.tgt_lang)
    return JsonResponse({'generated_text': title_text})

@router.post("/sentences")
def generate_story_continuationi(request, image: UploadedFile = File(...), 
                               prompt: Optional[str] = None, 
                               chapter_index: Optional[str] = None):
    # image to text caption generation
    generated_description = continue_story(pil_image=image,prompt=prompt) 
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/completions")
def generate_complete_sentence(request, image: UploadedFile = File(...), 
                               prompt: Optional[str] = None):
    # image to text caption generation
    generated_description = complete_sentence(pil_image=image,prompt=prompt) 
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/captions")
def create_image_caption(request, image: UploadedFile = File(...)):
    caption = image_caption(image)
    return JsonResponse({'caption': caption})