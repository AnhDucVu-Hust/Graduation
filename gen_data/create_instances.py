from gpt_api import call_gpt
from openai import OpenAI
import random
import time
from utils import  *
import json
from templates.context_gen_template import template_instances,prompt_instance
with open("../data/jssp/jssp.json", "r", encoding="UTF-8") as f:
    data = json.load(f)
openai.api_key="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"
def response_parser(response):
    choice = response.choices[0]
    if choice.finish_reason != 'stop':
        return None
    else:
        content = choice.message.content
    content = content.split("#")
    if len(content)==3:
        job = content[2]
        machine = content[1]
        jobs =job.strip().split("\n")[1:]
        machines = machine.strip().split("\n")[1:]
    else:
        return False
    return machines,jobs

def post_processing_response(response):
    choice = response.choices[0]
    if choice.finish_reason != 'stop':
        return None
    else:
        content = choice.message.content
        content = content.strip('Problem: ')
        return content
def create_prompt(context,param):
    processing_time = ''
    for id in range(param['jobs']):
        detail = param['details'][id]
        detail_str = ["Machine "+ str(x["machine_id"]+1)+": "+str(x['processing_time']) for x in detail["tasks"]]
        detail_str = ', '.join(detail_str)
        #processing_time += f"Job{id + 1}: {detail_str}\n"
    prompt = prompt_instance.format(context=context, m=param['machines'], j=param['jobs']) #processing_time=processing_time)
    #prompt += "Remember to check if your example is completely comprehensive and have all parameters i provide above. If not, you need to complete it. Don't response a paragraph with just some job's processing time and say 'continue for another...'"
    print(prompt)
    return prompt
client = OpenAI()
contexts=[]
with open("../data/generated_contexts/generated_contexts_gpt.jsonl", 'r') as json_file:
    for line in json_file:
        contexts.append(json.loads(line))
instance_file_path = '../data/instaces/'
os.makedirs(instance_file_path,exist_ok=True)
if os.path.exists(os.path.join(instance_file_path,"instances_v2.jsonl")):
    with open(os.path.join(instance_file_path,"instances_v2.jsonl"),"r",encoding="UTF-8") as f:
        json_list = list(f)
        samples=[]
        for json_str in json_list:
            print(json_str)
            json_info = json.loads(json_str)
            if json_info['problem']['jobs']<16:
                samples.append(json_info)
        len_instance = len(samples)
        problem_count = [data['problem']['name'] for data in samples]
        problem_count = {x:problem_count.count(x) for x in problem_count}
        print(problem_count)

else:
    len_instance = 0
    problem_count = {}
from tqdm import tqdm

with tqdm(initial=len_instance, desc='Writing to JSON', unit='iteration') as pbar:
    for x in data:
        if x["jobs"]>15:
            continue
        if x["name"] in problem_count.keys():
            len_sample = 9 - problem_count[x["name"]]
        else:
            len_sample = 9
        sample_contexts = random.sample(contexts,len_sample)
        sample_contexts = [context["instruction"] for context in sample_contexts]
        print(f"Machines:{x['machines']}")
        print(f"Jobs:{x['jobs']}")
        print(f"Detail:{x['details']}")
        for context in sample_contexts:
            start_time =time.time()
            prompt = create_prompt(context,x)
            from openai import OpenAI
            messages = template_instances
            messages[1]['content'] = prompt
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages= messages,
                temperature=0.5,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response.choices[0].message.content)
            new_instance = response_parser(response)
            print(new_instance)
            if new_instance:
                machines,jobs = new_instance
                new_instance = {'machines':machines,'jobs':jobs,'problem':x,'context':context}
                if new_instance != None:
                    with open(os.path.join(instance_file_path,"instances_v2.jsonl"),"a",encoding="UTF-8") as f:
                        json.dump(new_instance,f)
                        f.write("\n")
                        pbar.update(1)
                        #print("####Paragraph###")
                        #print(new_instance['paragraph'])

            elapsed_time = time.time() - start_time
            remaining_time = 20 - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)
            print("##############")

