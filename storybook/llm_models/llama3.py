import transformers
import torch

model_id = "unsloth/llama-3-8b-Instruct-bnb-4bit"
pipeline = transformers.pipeline(
    "text-generation",
    model="/home/aidev/Documents/back-end/storybookcreator/LLM_models/llama3/",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    )

messages = [
            {
                "role": "system",
                "content": "You help creating a book for children" ,
            },
            {"role": "user", "content":'''Write a short prompt for a children's book. The prompt should be easily understood by children and be an open ended sentence ending with "...". Follow a similar style as in the examples.
Example 1: Wanda is a witch. She always ...
Example 2: Edgar the elephant loves music. He plays ... . 
Example 3: Ratty lives in a dustbin. He dreams of being ... 
Example 4: I love to stay at grandma's house. She always ..."
Now write a prompt about Wanda, the witch. '''}
        ]


def generate_chapters(user_input: str) -> str:
    prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=1.5,
    top_p=0.9,
    )
    return outputs[0]["generated_text"][len(prompt):]
    


def merge_sentences(user_input: str, img_caption: str, temperature: float, ch_index: str) -> str:
    messages = [
            {
                "role": "system",
                "content": "You help writing sentences for a children's book. The sentences should be very simple to be easily understandable and in correct english grammar." ,
            },
            {"role": "user", "content":'''Combine two sentences into a meaningful story. Follow the examples in text length and style.
Example 1: Sentence: Wanda is a witch. She always ... Image: a girl in a blue dress. Completion: Wanda is a witch. She always wears a blue dress.
Example 2: Sentence: Wanda is a witch. She always ... Image: a girl dressed in a pink dress and a hat. Completion: Wanda is a witch. She always wears a blue dress.
Example 3: Sentence: Wanda is a witch. She always ... wears a girl in a green dress and has a broomstick. Completion: Wanda is a witch. She always wears a green dress and has a broomstick.
Now combine the following input Sentence: ''' +  user_input + " Image: "+  img_caption + " Completion:"}
        ]
    pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    )
    prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    outputs = pipeline(
    prompt,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=1.5,
    top_p=0.9,
    )
    output = outputs[0]["generated_text"][len(prompt):]
    print(output)
    length = output.count('\n')
    if length > 1:
        
        output = output.split('\n')[1]
        

    return output