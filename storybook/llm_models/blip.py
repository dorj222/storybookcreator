from transformers import BlipProcessor, BlipForConditionalGeneration
from storybook.llm_models.tiny_llama import generate_description_story
from storybook.llm_models.mistral import generate_description_story_mistral
from storybook.llm_models.phi2 import generate_description_story_msft_phi2
from storybook.llm_models.phi2_dolphin import generate_description_story_dolphin_phi2
from storybook.llm_models.gemma import generate_description_story_gemma
from PIL import Image as PILImage
import torch
import gc

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_image_description(pil_image, prompt, chapter_index):
    gc.collect()
    torch.cuda.empty_cache()
    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    text = "this is going to be a story of"
    inputs = processor(pil_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    image_caption = f"{prompt}; {image_caption}"
    # children_story = generate_description_story(image_caption, chapter_index)
    # children_story = generate_description_story_dolphin_phi2(image_caption, chapter_index)
    # children_story = generate_description_story_mistral(image_caption, chapter_index)
    # children_story = generate_description_story_dolphin_phi2(image_caption, chapter_index)
    children_story = generate_description_story_gemma(image_caption, chapter_index)
    
    gc.collect()
    torch.cuda.empty_cache()
    return children_story

def generate_image_caption(pil_image):
    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    text = "this is a children drawing of"
    inputs = processor(pil_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    image_caption = image_caption.split("this is a children drawing of")[1]
    gc.collect()
    torch.cuda.empty_cache()
    return image_caption