from diffusers import StableDiffusionXLImg2ImgPipeline
from PIL import Image
import torch
import json
import os
import gc

config_path = os.path.join(os.path.dirname(__file__), "../../img2img_models", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

def run(image, prompt):
    image = image.resize((512, 512))
    torch.cuda.empty_cache()
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(config["sd_turbo_path"],
                                                             strength=config["strength"],
                                                             guidance_scale=config["guidance_scale"],
                                                             num_inference_steps=config["num_inference_steps"],
                                                             torch_dtype=torch.float16, variant="fp16").to("cuda")
    #pipe.load_lora_weights(config["lora_path"])
    image = pipe(prompt, image=image, strength=config["strength"]).images[0]
    # Immediately delete the pipe object
    del pipe
    # Perform garbage collection
    gc.collect()
    torch.cuda.empty_cache()
    return image