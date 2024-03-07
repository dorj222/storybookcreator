import torchaudio
from transformers import AutoProcessor, SeamlessM4TModel
import torch
import gc



def translate_text(user_input: str, tgt_lang) -> str:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
    model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")
    model = model.to(device)
    text_inputs = processor(text = user_input, src_lang="eng", return_tensors="pt")
    text_inputs = {k: v.to(device) for k, v in text_inputs.items()}
    output_tokens = model.generate(**text_inputs, tgt_lang=tgt_lang, generate_speech=False)
    translated_text_from_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    gc.collect()
    del model 
    torch.cuda.empty_cache()
    return translated_text_from_text