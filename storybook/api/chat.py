# views.py
from ninja import Router
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from typing import Optional

from storybook.schema import GenerateTextSchema, TranslateTextSchema, GenerateStorySchema
from storybook.llm_models.tiny_llama import generate_title
from storybook.llm_models.tiny_llama import generate_description_story
from storybook.llm_models.seamless import translate_text
from storybook.llm_models.blip_instruct import complete_sentence, image_caption

router = Router()
@router.post("/titles")
def generate_storybook_title(request, data: GenerateTextSchema):
    title_text = generate_title(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/translations")
def generate_translations(request, data: TranslateTextSchema):
    title_text = translate_text(data.user_input, data.tgt_lang)
    return JsonResponse({'generated_text': title_text})

@router.post("/chapterstories")
def generate_complete_sentence(request, ch_index: Optional[str] = None ,prompt: Optional[str] = None):
    generated_description = generate_description_story(user_input=prompt, ch_index=ch_index)
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/fullsentences")
def generate_complete_sentence(request, image: UploadedFile = File(...), 
                               prompt: Optional[str] = None):
    generated_description = complete_sentence(pil_image=image,prompt=prompt) 
    response_data = {
        "generated_description": generated_description
    } 
    return JsonResponse(response_data)

@router.post("/captions")
def create_image_caption(request, image: UploadedFile = File(...)):
    caption = image_caption(image)
    print("CAPTION: "  + caption)

    return JsonResponse({'caption': caption})