from diffusers import StableDiffusionXLImg2ImgPipeline
import torch
import json
import os
import gc

config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)


pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(config["sd_turbo_path_fp16"],
                                                            torch_dtype=torch.float16, 
                                                            variant="fp16",
                                                            use_safetensors=True,                                                           
                                                             guidance_scale=0.0,
                                                             num_inference_steps=10
                                                             ).to("cuda")
def run(image, prompt, strength):
    
    torch.cuda.empty_cache()
    gen_image = pipe(prompt, image=image, strength=strength, guidance_scale=0.0,
                                                             num_inference_steps=10).images[0]
    # Perform garbage collection
    #gc.collect()
    #torch.cuda.empty_cache()
    return gen_image