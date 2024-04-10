import sys
sys.path.append("..")
import json
import time
from openai import OpenAI
import openai
from templates.context_gen_template import *
def create_prompt(context,param):
    processing_time = ''
    machines = param['machines']
    jobs = param['jobs']
    if len(machines) != param['problem']['machines'] or len(jobs) != param['problem']['jobs']:
        return None

    for id in range(param['problem']['jobs']):
        detail = param['problem']['details'][id]
        detail_str = [machines[x["machine_id"]]+": "+str(x['processing_time']) for x in detail["tasks"]]
        detail_str = ', '.join(detail_str)
        processing_time += f"{jobs[id]}: {detail_str}\n"
    prompt = prompt_instance_v2.format(context=context,processing_time=processing_time)
    #prompt += "Remember to check if your example is completely comprehensive and have all parameters i provide above. If not, you need to complete it. Don't response a paragraph with just some job's processing time and say 'continue for another...'"
    #print(prompt)
    return prompt
import os
os.environ["OPENAI_API_KEY"]="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"
if os.path.exists("../data/instaces/instances_full_v2.jsonl"):
    with open("../data/instaces/instances_full_v2.jsonl") as f:
        existed_data = []
        for line in f:
            json_data = json.loads(line)
            existed_data.append(json_data)
        problem_count = [data['index'] for data in existed_data]
        problem_count = {x: problem_count.count(x) for x in problem_count}
else:
    problem_count={}

with open("../data/instaces/instances_v2.jsonl", "r", encoding="UTF-8") as f:
    for index,line in enumerate(f):
        dict_data = json.loads(line)
        prompt = create_prompt(dict_data["context"],dict_data)
        if prompt == None:
            continue


        messages = template_instances_v2
        messages[1]['content'] = prompt.split("\n")[0]
        client = OpenAI()
        if index in problem_count.keys():
            num_samp = 3-problem_count[index]
        else:
            num_samp = 3
        for _ in range(num_samp):
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            with open("../data/instaces/instances_full_v2.jsonl", "a", encoding="UTF-8") as f:
                content = response.choices[0].message.content+"\n" + prompt.split("#")[2].strip()
                json_data = {'index':index,'content':content}
                print(json_data)
                json.dump(json_data,f)
                f.write("\n")
            elapsed_time = time.time()-start_time
            remaining_time = 20 - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)