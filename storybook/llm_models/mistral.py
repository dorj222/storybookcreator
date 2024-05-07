from transformers import AutoModelForCausalLM, AutoTokenizer
import torch



def m_continue_story(prompt):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16, load_in_8bit=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

    messages = [
    {"role": "user", "content": "Help me write a children's book story continuation by considering the input sentence. The story continuation has to be one sentence in total and be an incomplete sentence ending with '...'. \n\nExample1 \nInput sentence: Wanda is a witch. She always wears a blue dress.\nStory Continuation:"},
    {"role": "assistant", "content":"One day wanda wanders into the forest, she encounters a ..."},
    {"role": "user", "content": "\n\nExample2 \nInput sentence: Wanda is a witch. She always wears a red dress.\nStory Continuation:"},
    {"role": "assistant", "content":"One day wanda crafts a potion with ..."},
    {"role": "user", "content":  "\n\nExample3 \nInput sentence: Wanda is a witch. She always wears a witch's hat.\nStory Continuation:"},
    {"role": "assistant", "content":"One day wanda goes on a journey with her animal familiar, a ..."}]

    mistral_prompt = {"role": "user", "content": "\n\nInput sentence: " + prompt + "\nStory Continuation:"}
    messages.append(mistral_prompt)
    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

    model_inputs = encodeds#.to("cuda")
    #model.to("cuda")

    generated_ids = model.generate(model_inputs, max_new_tokens=64, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    generated_story = decoded[0].split("[/INST]")[-1]
    print(generated_story)
    if "(to be continued)" in generated_story:
        generated_story = generated_story.replace("(to be continued)", " ")
    if "</s>" in generated_story:
        generated_story = generated_story.replace("</s>", " ")
    
    if "(" in generated_story:
        generated_story = generated_story.split("(")[0]
    if "\n" in generated_story:
        generated_story = generated_story.split("\n")[0]

    return generated_story
