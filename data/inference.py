from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
import torch
access_token="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"
model_id = "google/gemma-2b"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
tokenizer = AutoTokenizer.from_pretrained(model_id,token=access_token)
tokenizer.pad_token = tokenizer.eos_token
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    trust_remote_code=True,
    token = access_token # Using this version because running the new version gives error
)
import numpy as np

texts_count = {str(i): 10 for i in range(11)}
texts = texts_count.keys()

device = "cuda:0"
def prob_decode(input_ids, texts):
    next_logits = {}
    input_text = tokenizer.decode(input_ids)
    tokenized_texts = {text: tokenizer(text, add_special_tokens=False)['input_ids'] for text in texts}
    score = {text: 1 for text in texts}
    for text, token in zip(tokenized_texts.keys(), tokenized_texts.values()):
        temp_text = input_text
        for tok in token:
            if temp_text not in next_logits.keys():
                outputs = base_model(**input_ids)
                next_token_logits = outputs.logits[:, -1, :]
                next_token_logits = torch.nn.functional.softmax(next_token_logits[0])
                next_logits[temp_text] = next_token_logits

            score[text] *= next_logits[temp_text][tok].cpu().detach().numpy()
            temp_text += tokenizer.decode(tok)
            input_ids = torch.cat((input_ids,tok),dim=-1)
    for text in texts:
        score[text] = np.power(score[text], 1 / len(tokenized_texts[text]))

    return score

def generate_solution(input_text,text_count):
    while len(text_count.keys())>0:
        input_ids = tokenizer(input_text, return_tensors="pt").to(device)
        copy_input_ids = input_ids.clone().detach()
        score = prob_decode(copy_input_ids,list(text_count.keys()))
        chosen_text = max(score,key=score.get)
        input_ids = torch.cat((input_ids,tokenizer(chosen_text, add_special_tokens=False,return_tensors='pt')['input_ids']),dim=-1)
        if text_count[chosen_text]==1:
            text_count.pop(chosen_text)
        else:
            text_count[chosen_text] -=1
    return input_text
if __name__=="__main__":
    import time

    instruction = """I will give you a Job Shop Scheduling Problem (JSSP) and  5 solutions for it.

    The solution will be encoded as a sequence of jobs, the ith occurrence of the job corresponding to the ith operation.

    Follow these step-by-step
    1. Select two parent solutions for crossover.
    2. Perform a crossover operation to create two offspring solutions.
    3. Apply a mutation operation to the offspring solutions. Then repeat from Step 1 multiple time to have 5 offspring solutions
    4. Response the offspring solutions `
<solution>7,5,4,1,2,6,7,0,2,1,4,5,9,2,8,2,3,0,0,0,9,4,2,5,6,7,7,3,9,5,1,2,1,4,0,4,7,3,1,3,9,3,6,6,4,8,8,9,8,1,2,1,7,7,4,3,0,9,7,1,8,9,2,5,6,3,4,4,3,5,5,2,2,4,0,6,8,3,5,1,6,0,9,7,6,0,8,3,7,5,6,6,0,8,5,8,9,9,1,8</solution>
<solution>7,5,2,6,2,5,0,9,9,2,9,6,8,8,2,0,8,5,4,6,0,9,0,0,9,9,7,6,7,1,9,3,4,0,7,3,1,2,9,2,6,4,0,1,9,5,7,7,7,3,6,8,2,8,3,5,4,2,8,6,5,2,4,3,1,1,6,7,4,5,3,8,4,2,3,1,4,4,0,4,5,3,5,8,8,7,5,3,3,8,6,1,9,1,7,1,0,1,6,0</solution>
<solution>5,5,3,0,4,5,0,1,0,1,8,4,6,4,7,1,2,1,5,7,8,4,2,1,9,9,9,2,3,5,0,2,9,6,8,9,9,2,2,7,3,0,7,8,6,1,6,5,8,3,8,3,7,6,5,1,2,5,8,4,9,6,0,7,6,3,4,7,0,9,1,8,5,2,0,5,8,2,6,3,7,6,0,4,1,8,9,2,0,9,6,4,3,7,1,4,3,4,7,3</solution>
<solution>2,9,3,3,9,0,4,6,3,6,5,4,5,2,0,3,1,7,8,9,9,2,7,7,1,7,4,4,5,8,9,3,8,0,8,1,1,0,1,6,8,7,6,2,4,6,0,3,2,3,5,1,0,4,7,0,9,2,2,3,9,5,5,2,4,1,4,6,7,6,1,1,3,4,7,0,1,6,0,2,5,4,9,3,6,8,9,5,8,9,8,8,2,7,0,7,6,5,5,8</solution>
<solution>7,0,7,9,5,1,6,4,3,7,0,8,6,6,9,5,7,8,3,4,5,4,1,8,5,0,3,4,9,6,7,9,6,1,3,3,9,4,7,2,7,2,7,3,6,8,2,1,5,0,6,0,5,3,1,1,5,0,1,9,8,9,6,4,8,4,7,8,5,2,9,1,6,8,2,2,7,0,3,9,9,1,4,2,2,8,0,5,8,6,2,4,5,0,3,4,2,0,3,1</solution>
<solution>2,8,1,6,6,2,3,9,8,7,3,6,5,2,1,5,3,2,0,1,9,5,1,4,8,0,9,0,7,8,2,5,6,7,6,0,2,9,8,6,4,9,5,3,2,5,0,3,6,0,2,7,1,8,7,7,4,1,4,9,4,2,3,4,6,9,1,5,4,8,0,7,8,8,5,5,0,7,6,6,9,0,8,9,1,0,4,5,3,7,1,1,9,2,3,7,4,3,3,4</solution>
<solution>8,7,2,3,7,4,2,1,9,9,8,9,6,6,4,5,8,2,3,2,2,0,0,3,2,9,2,3,0,9,3,7,8,1,5,6,5,7,9,8,3,7,4,7,3,5,9,4,9,1,2,6,6,6,1,0,0,7,5,3,2,0,7,4,4,5,5,8,8,0,4,1,0,8,6,7,0,1,6,0,5,7,3,4,2,3,9,6,9,5,1,1,1,6,8,4,8,4,1,5</solution>
<solution>4,4,6,2,1,7,6,7,8,2,8,1,1,3,9,2,4,3,5,5,5,8,6,0,9,3,2,4,4,3,3,8,4,4,7,7,3,7,4,9,5,9,2,6,2,0,5,7,1,8,9,9,8,1,9,5,8,4,7,0,1,5,6,2,1,7,0,2,1,1,9,5,1,6,6,0,8,6,6,0,3,3,0,9,9,0,6,3,4,5,7,8,7,0,3,2,5,8,0,2</solution>
<solution>5,8,2,1,2,3,8,6,6,5,8,7,7,8,5,1,2,8,1,0,5,0,9,7,0,0,5,4,9,1,0,7,4,3,5,4,4,6,3,3,9,1,7,5,6,2,4,1,9,2,7,3,4,9,6,4,6,9,7,3,6,9,3,5,2,9,5,4,2,1,3,8,3,8,5,2,0,2,6,9,1,0,3,0,1,7,4,2,8,0,6,0,9,8,8,7,7,4,6,1</solution>
<solution>8,0,2,6,3,2,4,5,5,0,3,2,0,5,0,5,0,7,6,7,7,1,0,5,8,4,5,7,6,9,2,3,9,3,9,8,9,4,6,8,3,1,1,4,3,7,7,4,6,1,1,9,7,8,5,1,4,8,4,0,3,6,9,2,0,9,2,0,2,5,7,4,1,0,3,8,7,5,2,6,8,2,4,5,1,6,9,8,9,1,6,2,6,7,3,4,8,9,1,3</solution>
<solution>6,7,2,6,0,9,1,0,1,4,2,0,7,1,2,5,1,2,0,4,8,6,6,9,0,5,5,7,1,5,7,8,3,0,3,4,9,1,8,3,7,2,8,4,9,5,4,7,0,5,9,8,4,3,9,6,2,4,0,5,2,8,6,1,3,8,3,3,5,7,0,6,6,9,9,5,1,7,2,3,4,0,3,8,1,4,4,6,8,7,1,5,2,7,9,9,2,8,3,6</solution>
<solution>7,4,9,7,1,2,6,6,0,5,0,8,2,6,2,1,8,9,9,9,5,4,9,7,9,0,5,9,0,4,8,3,7,2,8,7,1,3,0,5,9,5,3,0,1,2,0,1,6,2,1,7,8,4,6,1,6,2,8,3,8,5,2,4,2,2,3,5,0,8,3,3,3,7,3,4,6,7,4,1,7,9,4,1,1,6,4,4,5,9,8,3,5,5,0,6,6,7,0,8</solution>
<solution>6,0,9,3,1,6,9,2,4,9,9,6,5,1,6,2,6,4,4,8,5,7,2,6,1,4,8,3,8,4,9,3,0,3,9,8,0,0,8,3,8,5,7,2,6,0,5,1,0,9,7,6,5,8,3,2,1,1,7,5,1,3,6,4,4,8,3,0,9,2,3,5,8,5,0,2,6,5,0,2,7,7,1,5,7,1,0,4,4,7,4,7,9,1,8,9,7,2,3,2</solution>
<solution>4,4,9,7,7,9,8,6,7,5,9,2,2,7,3,3,1,8,0,5,2,8,9,7,5,3,4,6,8,0,2,0,8,5,3,3,1,0,7,2,0,9,0,1,9,9,4,6,3,1,2,7,6,1,9,8,8,2,8,1,4,6,5,6,4,9,6,6,3,3,4,9,0,5,2,0,5,7,1,1,5,8,8,6,5,4,2,1,2,1,3,7,0,7,5,4,4,6,0,3</solution>
<solution>2,9,2,4,9,6,4,9,9,7,4,0,7,1,1,3,0,7,5,6,4,6,4,4,3,2,5,4,4,6,9,1,6,9,7,6,7,3,9,7,9,2,6,1,7,3,8,3,0,6,8,9,3,8,0,3,3,8,4,8,0,8,2,6,1,1,5,5,0,0,7,2,5,1,2,5,8,9,8,8,4,1,5,2,8,1,7,5,2,0,5,0,0,3,3,7,6,1,2,5</solution>
<solution>2,5,6,2,3,0,4,9,7,9,4,0,4,1,6,1,5,7,0,2,6,4,7,1,8,5,4,5,0,9,9,3,6,8,1,8,6,8,2,5,4,8,9,9,7,8,2,5,9,8,0,2,2,4,6,3,6,6,5,5,6,1,0,3,9,2,1,1,8,7,7,1,1,3,3,3,3,4,7,7,4,9,0,7,2,7,8,0,0,2,9,6,8,4,5,3,1,0,3,5</solution>
    """
    texts_count = {str(i): 10 for i in range(10)}
    start_time = time.time()
    print(generate_solution(instruction, texts_count))
    print(f"Generate in {time.time() - start_time}s")