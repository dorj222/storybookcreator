from ninja import Router, Schema
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from storybook.schema import GenerateTextSchema

import torch
import gc

import os
os.environ["CUDA_HOME"] = "/usr/local/cuda"

import torch
assert torch.cuda.is_available()
assert torch.backends.cudnn.enabled




def generate_description_story_mistral(user_input: str, chapter_index) -> str:
    model_name_or_path = "TheBloke/Mistral-7B-OpenOrca-GPTQ"
    
    # Load OpenOrca model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto", trust_remote_code=False, revision="main")
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    device = "cuda" 
    model.to(device)
    
    gc.collect()
    torch.cuda.empty_cache()

    system_message = "You are my children's storybook narrator. " + chapter_index 
    prompt = user_input
    prompt_template=f'''<|im_start|>system
    {system_message}<|im_end|>
    <|im_start|>user
    {prompt}<|im_end|>
    <|im_start|>assistant
    '''

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    outputs = model.generate(inputs=input_ids, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=40, top_p=0.95, repetition_penalty=1.1)
    generated_text = tokenizer.decode(outputs[0])
    gc.collect()
    torch.cuda.empty_cache()
    generated_text.strip()
    generated_text = generated_text.split('user\n', 1)
    return generated_text[1]

def generate_title(user_input: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are my storybook title generator. Please only respond the storybook title with Title: keyword",
        },
        {"role": "user", "content": user_input},
    ]
    
    content = ' '.join([message['content'] for message in messages])
    input_ids = tokenizer(content, return_tensors='pt').input_ids.cuda()
    
    outputs = model.generate(inputs=input_ids, max_new_tokens=256)
    generated_text = tokenizer.decode(outputs[0])

    # Extract the first line (title) of the generated text
    title = generated_text.split("\n")[0].strip()
    # Remove 'Title: ' prefix if it exists
    if title.startswith("Title: "):
        title = title[len("Title: "):]
    gc.collect()
    torch.cuda.empty_cache()
    return title