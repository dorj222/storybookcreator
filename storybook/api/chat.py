# views.py
from ninja import Router, Schema
from django.http import JsonResponse

from storybook.schema import GenerateTextSchema, TranslateTextSchema
from storybook.llm_models.tiny_llama import generate_title
from storybook.llm_models.seamless import translate_text

router = Router()
@router.post("/titles")
def generate_storybook_title(request, data: GenerateTextSchema):
    title_text = generate_title(data.user_input)
    return JsonResponse({'generated_text': title_text})

@router.post("/translations")
def generate_translations(request, data: TranslateTextSchema):
    title_text = translate_text(data.user_input)
    return JsonResponse({'generated_text': title_text})