from ninja import Router, Schema
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from storybook.schema import GenerateTextSchema
from transformers import AutoModelForCausalLM, AutoTokenizer

import torch
import gc

def generate_description_story_dolphin_phi2(user_input: str, chapter_index) -> str:
    gc.collect()
    torch.cuda.empty_cache()
    torch.set_default_device("cuda")
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

    system_message = "You are my children's storybook narrator. " + chapter_index 
    prompt = user_input

    prompt_template=f'''<|im_start|>system
    {system_message}<|im_end|>
    <|im_start|>user
    {prompt}<|im_end|>
    <|im_start|>assistant
    '''

    inputs = tokenizer(prompt_template, return_tensors="pt", return_attention_mask=False)

    outputs = model.generate(**inputs, max_length=256)
    generated_text = tokenizer.batch_decode(outputs)[0]
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