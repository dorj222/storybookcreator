from diffusers import StableDiffusionXLImg2ImgPipeline
from PIL import Image

#configuration - todo: setup proper config file
model_path = "image2image/models/realcartoonXL_v2.safetensors"
strength = 0.9

def run(image, prompt):
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(model_path)
    pipe.to("cuda")
    image = pipe(prompt, image=image, strength=strength).images[0]
    #image.show() # Uncomment to show the image on the screen
    return image
