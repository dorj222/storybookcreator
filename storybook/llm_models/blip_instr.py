from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
from PIL import Image as PILImage
import torch
import gc

def complete_sentence(pil_image, prompt):
    gc.collect()
    torch.cuda.empty_cache()

    pil_image = PILImage.open(pil_image)
    pil_image = pil_image.convert("RGB").resize((512, 512))

    processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
    model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b", load_in_8bit=True)
    inputs = processor(images=pil_image, text=prompt, return_tensors="pt").to(device="cuda")

    # autoregressively generate an answer
    outputs = model.generate(
            **inputs,
            num_beams=5,
            max_new_tokens=256,
            min_length=1,
            top_p=0.9,
            repetition_penalty=1.5,
            length_penalty=1.0,
            temperature=1,
    )
    #outputs[outputs == 0] = 2 # this line can be removed once https://github.com/huggingface/transformers/pull/24492 is fixed
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    print(generated_text)
    del processor
    del model
    return generated_text
