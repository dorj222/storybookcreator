from diffusers import StableDiffusionXLImg2ImgPipeline
import torch
import json
import os
import gc

config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

def run(image, prompt, parameter):
    torch.cuda.empty_cache()
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(config["sd_turbo_path"],
                                                             strength=config["strength"]  * parameter,
                                                             guidance_scale=config["guidance_scale"],
                                                             num_inference_steps=config["num_inference_steps"] * parameter
                                                             ).to("cuda")
    # pipe.load_lora_weights(config["lora_path"])
    image = pipe(prompt, image=image, strength=config["strength"]).images[0]
    # image.show()
    # Immediately delete the pipe object
    del pipe
    # Perform garbage collection
    gc.collect()
    torch.cuda.empty_cache()
    return image