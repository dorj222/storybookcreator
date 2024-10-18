# views.py
from ninja import Router
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from typing import Optional

from storybook.schema import GenerateTextSchema, TranslateTextSchema, GenerateStorySchema
from storybook.llm_models.tiny_llama import generate_title
from storybook.llm_models.phi3 import merge_sentences, generate_chapters
from storybook.llm_models.seamless import translate_text
from storybook.llm_models.blip import generate_image_caption

router = Router()
@router.post("/titles")
def generate_storybook_title(request, data: GenerateTextSchema):
    title_text = generate_title(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/translations")
def generate_translations(request, data: TranslateTextSchema):
    title_text = translate_text(data.user_input, data.tgt_lang)
    return JsonResponse({'generated_text': title_text})

@router.post("/chapters")
def generate_chapter_completion(request, image: UploadedFile = File(...), prompt: Optional[str] = None, temperature: Optional[float] = None, ch_index: Optional[str] = None):
    caption = generate_image_caption(image)

    generated_description = merge_sentences(user_input = prompt, img_caption=caption, temperature = temperature, ch_index=ch_index) 
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/captions")
def create_image_caption(request, image: UploadedFile = File(...)):
    caption = generate_image_caption(image)
    return JsonResponse({'caption': caption})

@router.post("/nextprompts")
def generate_next_prompts(request, prev_story):
    next_prompt = generate_chapters(prev_story)
    return JsonResponse({'next_prompt': next_prompt})