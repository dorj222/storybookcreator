# views.py
from ninja import Router, Schema
from django.http import JsonResponse
from transformers import pipeline
import torch
from storybook.schema import GenerateTextSchema
router = Router()

# Load TinyLlama model
pipe = pipeline("text-generation", 
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                torch_dtype=torch.bfloat16, 
                device_map="auto")

@router.post("/titles")
def generate_text(request, data: GenerateTextSchema):
    # Get user input from the request
    user_input = data.user_input
    messages = [
        {
            "role": "system",
            "content": "You are my storybook title generator. Your response is limited to only the storybook title. Please limit entire your response to 20 characters.",
        },
        {"role": "user", "content": user_input},
    ]

    # Apply chat template and generate text
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

    # Extract the generated text
    generated_text = outputs[0]["generated_text"]
    return JsonResponse({'generated_text': generated_text})