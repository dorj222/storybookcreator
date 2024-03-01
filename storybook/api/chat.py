# views.py
from ninja import Router, Schema
from django.http import JsonResponse
from ninja import Router, File
from ninja.files import UploadedFile
from PIL import Image as PILImage


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

@router.post("/story")
def create_story(request, data:GenerateStorySchema):
    # image to text caption generation
    generated_stpry = generate_image_description(Caption=data["caption"], prompt=data["prompt"], chapter = data["chapter"]) 
    response_data = {
        "story": generated_stpry
    } 
    return 201, response_data

@router.post("/caption")
def create_image_caption(request, image: UploadedFile = File(...)):
    pil_image = PILImage.open(image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    caption = generate_image_caption(pil_image)
    return JsonResponse({'caption': caption})