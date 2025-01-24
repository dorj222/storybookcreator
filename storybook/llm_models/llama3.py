from ninja import Router, Schema
from django.http import JsonResponse
from transformers import pipeline
from storybook.schema import GenerateTextSchema
import json

import os
import gc
import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
# Import config file
config_path = os.path.join(os.path.dirname(__file__), "../../", "config.json")
# Load configuration from config.json
with open(config_path, "r") as config_file:
    config = json.load(config_file)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

device="cuda"
torch.random.manual_seed(0)



def merge_sentences(user_input: str, img_caption: str, temperature: float, ch_index: str, language: str) -> str:
    gc.collect()
    torch.cuda.empty_cache()

    if language == "ger":
            messages = [
            {
                "role": "system",
                "content": "Du bist der Erzähler meines Kinderbuchs." ,
            },
            {"role": "user", "content": "Kombiniere die Folgenden beiden Sätze in einer Fortsetzung" + "Satz 1: " + user_input  + ". Satz 2: " + img_caption + ". Fortsetzung:"}
        ]

    
    else:

        messages = [
                {
                    "role": "system",
                    "content": config["narrator_prompt_start"] ,
                },
                {"role": "user", "content": config["merge_sentences"] + "Sentence 1: " + user_input  + ". Sentence 2: " + img_caption + ". Complete:"}
            ]
    print(messages)
    model = AutoModelForCausalLM.from_pretrained(
    "DiscoResearch/Llama3-DiscoLeo-Instruct-8B-v0.1",
    torch_dtype="bfloat16",
    device_map=device
    )
    tokenizer = AutoTokenizer.from_pretrained("DiscoResearch/Llama3-DiscoLeo-Instruct-8B-v0.1")

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    # Apply chat template and generate texts
    del model
    del tokenizer
    del model_inputs
    del generated_ids

    gc.collect()
    torch.cuda.empty_cache()

    return response

def generate_title(user_input: str, language: str) -> str:
    gc.collect()
    torch.cuda.empty_cache()
    if language == "ger":
        messages = [
        {
            "role": "system",
            "content": "Bitte betrachte den folgenden Text und erstelle einen Kinderbuch-Titel mit Titel: Stichwort",
        },
        {"role": "user", "content": user_input},
        ]

    else:
        messages = [
                {
                    "role": "system",
                    "content": config["title_prompt"],
                },
                {"role": "user", "content": user_input},
            ]
    model = AutoModelForCausalLM.from_pretrained(
    "DiscoResearch/Llama3-DiscoLeo-Instruct-8B-v0.1",
    torch_dtype="bfloat16",
    device_map=device
    )
    tokenizer = AutoTokenizer.from_pretrained("DiscoResearch/Llama3-DiscoLeo-Instruct-8B-v0.1")

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    # Apply chat template and generate texts
    del model
    del tokenizer
    del model_inputs
    del generated_ids
    gc.collect()
    torch.cuda.empty_cache()

    return response


def generate_chapters(user_input: str ) -> str:
    gc.collect()
    torch.cuda.empty_cache()

    messages = [
        {
            "role": "system",
            "content": config["narrator_prompt_start"] ,
        },
        {"role": "user", "content": "Continue the following story in one very short sentence.\nStory:" + user_input}
    ]

    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )
    outputs = pipe(prompt, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=50, top_p=0.95, repetition_penalty=1.3, length_penalty=0.5)
    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    assistant_index = generated_text.find("<|assistant|>")
    if assistant_index != -1:
        generated_text = generated_text.split('\n<|assistant|>\n', 1)
        generated_text = generated_text[1]
        # Remove "\n" from the generated text
        generated_text = generated_text.replace("\n\n", ". ")
        generated_text = re.sub(r'[!?]', '.', generated_text)
        print("generate_prompt_helper: ", generated_text)
        # Split the text into sentences
        sentences = generated_text.split('.')
        # Remove unqualified sentences
        gc.collect()
        torch.cuda.empty_cache()
        sentences = [sentence.strip() for sentence in sentences if sentence.strip() and len(sentence.strip().split()) > 1]
        if sentences[:1]:
            generated_text = '. '.join(sentences[:1]) + ". "
        gc.collect()
        torch.cuda.empty_cache()
        return generated_text
    else:
        return 'Chapter story not generated'

def generate_prompts(user_input: str) -> str:
    gc.collect()
    torch.cuda.empty_cache()
    generated_text = generate_chapters(user_input, "ch2")
    nltk.download('punkt')
    # Tag the tokens with their parts of speech
    tagged_tokens = pos_tag(word_tokenize(generated_text))
    # Extract verbs from the tagged tokens
    verbs = [word for word, pos in tagged_tokens if pos.startswith('V')]
    verb_indices = [i for i, token in enumerate(word_tokenize(generated_text)) if token in verbs]
    # Find the index of the middle verb occurrence
    index = verb_indices[len(verb_indices) // 2]
    # Construct the incomplete sentence ending with the middle verb
    incomplete_sentence = ' '.join(word_tokenize(generated_text)[:index + 1])
    gc.collect()
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.empty_cache()
    return incomplete_sentence