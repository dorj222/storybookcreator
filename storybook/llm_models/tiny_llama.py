from ninja import Router, Schema
from django.http import JsonResponse
from transformers import pipeline
import torch
from storybook.schema import GenerateTextSchema
import json

import os
import gc
import re

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

def generate_description_story(user_input: str , ch_index: str) -> str:
    messages = [
        {
            "role": "system",
            "content": config["narrator_prompt_start"] ,
        },
        {"role": "user", "content": config[ch_index] + user_input + config["narrator_prompt_end"] }
    ]

    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )
    outputs = pipe(prompt, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=50, top_p=0.95, repetition_penalty=1.3)
    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    generated_text = generated_text.split('\n<|assistant|>\n', 1)
    generated_text = generated_text[1]
    # Remove "\n" from the generated text
    generated_text = generated_text.replace("\n\n", ". ")
    generated_text = re.sub(r'[!?]', '.', generated_text)
    # Split the text into sentences
    sentences = generated_text.split('.')
    # Remove unqualified sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip() and len(sentence.strip().split()) > 1]
    print('sentences: ', sentences)
    # Check if the length of the generated text is more than 200 characters
    if sentences[0] and len(sentences[0]) > 140:
        generated_text = '. '.join(sentences[:1]) + ". "
    elif len(generated_text) > 200 and len(sentences) > 1:
        generated_text = '. '.join(sentences[:2]) + ". "
    else:
        generated_text = '. '.join(sentences[:3]) + ". " if len(sentences) > 2 else '.'.join(sentences)


    gc.collect()
    torch.cuda.empty_cache()
    return generated_text
    
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
    
def complete_initial_sentence(user_input: str, img_caption: str, temperature: float) -> str:
    messages = [
        {
            "role": "system",
            "content": config["narrator_prompt_start"] ,
        },
        {"role": "user", "content": config["complete_prompt_part1"] + " \n Sentence1: " + user_input  + "\nSentence2" + img_caption}
    ]
    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    outputs = pipe(prompt, max_new_tokens=64, do_sample=True, temperature=temperature, top_k=50, top_p=0.95)
    print(outputs)
    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    # Find the assistant's response start index
    assistant_index = generated_text.find("<|assistant|>")
    gc.collect()
    torch.cuda.empty_cache()
    
    if assistant_index != -1:
        # Get the assistant's response
        assistant_response = generated_text[assistant_index + len("<|assistant|>"):]
        # Remove Complete keyword if present
        if "Complete:" in assistant_response:
            assistant_response=assistant_response.removeprefix('\nComplete:')
        return assistant_response
    else:
        return 'Text not generated'