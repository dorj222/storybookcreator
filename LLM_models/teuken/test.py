import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "openGPT-X/Teuken-7B-instruct-commercial-v0.4"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
)
model = model.to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_fast=False,
    trust_remote_code=True,
)
messages = [{"role": "User", "content": "Wer bist du?"}]
prompt_ids = tokenizer.apply_chat_template(messages, chat_template="DE", tokenize=True, add_generation_prompt=True, return_tensors="pt")
prediction = model.generate(
    prompt_ids.to(model.device),
    max_length=512,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.7,
    num_return_sequences=1,
)
prediction_text = tokenizer.decode(prediction[0].tolist())
print(prediction_text)