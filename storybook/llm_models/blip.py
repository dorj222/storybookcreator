from transformers import BlipProcessor, BlipForConditionalGeneration
from storybook.llm_models.tiny_llama import generate_description_story

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_image_description(pil_image):
    text = "this is a children drawing of"
    inputs = processor(pil_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    #children_story = generate_description_story(image_caption)
    return image_caption