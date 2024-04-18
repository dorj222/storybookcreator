from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
from PIL import Image as PILImage
import torch
import gc


processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b",torch_dtype=torch.float16, load_in_8bit=True)

def complete_sentence(pil_image, prompt):

    #processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
    #model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b",torch_dtype=torch.float16, load_in_8bit=True)

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    inputs = processor(images=pil_image, text=prompt, return_tensors="pt").to(device="cuda")

    outputs = model.generate(
            **inputs,
            num_beams=5,
            max_new_tokens=32,
            min_length=1,
            top_p=0.9,
            repetition_penalty=10.5,
            length_penalty=1.0,
            temperature=1,
    )
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    return generated_text

def continue_story(pil_image, prompt):
    #processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
    #model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b",torch_dtype=torch.float16, load_in_8bit=True)

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    
    prompt = "<Image> This is an image from a childrens book. Questions: Consider the following story:" + prompt +"\nContinue the story with one sentence:"
    inputs = processor(images=pil_image, text=prompt, return_tensors="pt").to(device="cuda")

    outputs = model.generate(
        **inputs,
        num_beams=5,
        max_new_tokens=32,
        min_length=1,
        top_p=0.9,
        repetition_penalty=10.0,
        length_penalty=2.0,
        temperature=1,
)
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    return generated_text

def image_caption(pil_image):
    #processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
    #model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b",torch_dtype=torch.float16, load_in_8bit=True)

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))
    
    prompt = "<Image> A short image description:"
    inputs = processor(images=pil_image, text=prompt, return_tensors="pt").to(device="cuda")

    outputs = model.generate(
        **inputs,
        num_beams=5,
        max_new_tokens=32,
        min_length=1,
        top_p=0.9,
        length_penalty=2.0,
        temperature=1,
)
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()

    return generated_text