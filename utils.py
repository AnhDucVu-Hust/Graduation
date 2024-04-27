import openai
import os
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
