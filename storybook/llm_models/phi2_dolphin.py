from ninja import Router, Schema
from django.http import JsonResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from storybook.schema import GenerateTextSchema
from transformers import AutoModelForCausalLM, AutoTokenizer

import torch
import json
import os
import gc

# Import config file
config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

def generate_description_story_dolphin_phi2(user_input: str, chapter_index) -> str:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = AutoModelForCausalLM.from_pretrained("cognitivecomputations/dolphin-2_6-phi-2", torch_dtype="auto", trust_remote_code=True)
    model = model.to(device)

    tokenizer = AutoTokenizer.from_pretrained("cognitivecomputations/dolphin-2_6-phi-2", trust_remote_code=True)
    
    system_message = "You are my children's storybook narrator. Please consider the next texts and continues a children's storybook story in the voice of a children's storybook narrator.", 
    prompt = user_input

    prompt_template=f'''<|im_start|>system
    {system_message}<|im_end|>
    <|im_start|>user
    {prompt}<|im_end|>
    <|im_start|>assistant
    '''
    inputs = tokenizer(prompt_template, return_tensors="pt", return_attention_mask=False)
    gc.collect()
    torch.cuda.empty_cache()

    inputs = {k: v.to(device) for k, v in inputs.items()}  # moving inputs to appropriate device
    
    outputs = model.generate(**inputs, max_length=256)
    generated_text = tokenizer.batch_decode(outputs)[0]
    # print(generated_text)
    return generated_text
    
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