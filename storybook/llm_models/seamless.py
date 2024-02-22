import torchaudio
from transformers import AutoProcessor, SeamlessM4TModel

processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

def translate_text(user_input: str) -> str:
    text_inputs = processor(text = user_input, src_lang="eng", return_tensors="pt")
    output_tokens = model.generate(**text_inputs, tgt_lang="deu", generate_speech=False)
    translated_text_from_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    return translated_text_from_text