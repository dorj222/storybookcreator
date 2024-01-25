from diffusers import StableDiffusionXLImg2ImgPipeline
from PIL import Image
import torch 
#configuration - todo: setup proper config file
model_path = "image2image/models/realcartoonXL_v6.safetensors"
lora_path = "image2image/models/picbookXLloraV1.safetensors"
strength = 0.80
config = "realcartoon" # | "XL" | "realcartoon"


def run(image, prompt):
    if config == "turbo":
        model_path = "image2image/models/sd_xl_turbo_1.0.safetensors"
    elif config == "realcartoon":
        model_path = "image2image/models/realcartoonXL_v6.safetensors"
    print("Generate picture for prompt: "+prompt)
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(model_path,strength=strength, guidance_scale=0.0, num_inference_steps=2).to("cuda") 
    pipe.load_lora_weights(lora_path)
    image = pipe(prompt, image=image, strength=strength).images[0]
    image.show() 
    return image
