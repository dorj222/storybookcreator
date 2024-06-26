from transformers import BlipProcessor, BlipForConditionalGeneration
from storybook.llm_models.tiny_llama import generate_description_story, complete_initial_sentence
from PIL import Image as PILImage
import torch
import gc


def generate_image_description(pil_image, prompt, chapter_index):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    inputs = processor(pil_image, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    image_caption = f"{image_caption}. {prompt}."
    children_story = generate_description_story(image_caption, chapter_index)
    gc.collect()
    torch.cuda.empty_cache()
    return children_story

def generate_initial_text(pil_image, prompt):
    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    text = "What do you see?"
    inputs = processor(pil_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    # image_caption = f"Additional helpful information: {image_caption}."
    image_caption = image_caption.replace("a drawing of", "").replace("a cartoon of", "")
    children_story = complete_initial_sentence(prompt, image_caption)
    gc.collect()
    torch.cuda.empty_cache()
    return children_story

def generate_image_caption(pil_image):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    text = "this is a drawing of"
    inputs = processor(pil_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    if text in image_caption:
        image_caption = image_caption.split(text)[1]
    gc.collect()
    torch.cuda.empty_cache()
    return image_caption