from ninja import Router, Schema
from django.http import JsonResponse
from transformers import pipeline
import torch
from storybook.schema import GenerateTextSchema
import json
import os
import gc

# Import config file
config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Load TinyLlama model
pipe = pipeline("text-generation", 
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                torch_dtype=torch.bfloat16, 
                device_map="auto")

def generate_description_story(user_input: str, chapter_index) -> str:
    messages = [
        {
            "role": "system",
            "content": config[chapter_index],
        },
        {"role": "user", "content": user_input},
    ]

    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )
    outputs = pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    # Remove "Narration:" and "\n\n" from the generated text
    generated_text = generated_text.replace("Narration:", "").replace("\n\n", "").replace("\n", "").replace("\\", "")
    # Select the first 3 sentences
    generated_text = generated_text.split('.')
    generated_text = ".".join(generated_text[:3])
    assistant_index = generated_text.find("<|assistant|>")
    gc.collect()
    torch.cuda.empty_cache()
    if assistant_index != -1:
        assistant_response = generated_text[assistant_index + len("<|assistant|>"):]
        return assistant_response.strip()
    else:
        return "Assistant response not generated"
    
def generate_title(user_input: str) -> str:
    messages = [
        {
            "role": "system",
            "content": config["title_prompt"],
        },
        {"role": "user", "content": user_input},
    ]

    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    # Find the assistant's response start index
    assistant_index = generated_text.find("<|assistant|>")
    gc.collect()
    torch.cuda.empty_cache()
    if assistant_index != -1:
        # Get the assistant's response
        assistant_response = generated_text[assistant_index + len("<|assistant|>"):]
        # Extract the first two lines (title) of the assistant's response
        title = "\n".join(assistant_response.split("\n")[:2]).strip()
        # Remove 'Title: ' prefix if it exists
        if title.startswith("Title: "):
            title = title[len("Title: "):]
        return title
    else:
        return 'Title not generated'