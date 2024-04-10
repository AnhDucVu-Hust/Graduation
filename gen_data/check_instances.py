import json
data = []
from create_instances import create_prompt
'''
with open("./data/instaces/instances.jsonl","r",encoding="UTF-8") as f:
    for line in f:
        json_data = json.loads(line)
        if 'continue' in json_data['paragraph']:
            json_data['prompt'] = create_prompt(context='',param=json_data['problem'])
            data.append(json_data)
data =[{'paragraph':x['paragraph'],'prompt':x['prompt'],'problem':x['problem']['name']} for x in data]
import pandas as pd
df = pd.DataFrame(data)
df.to_excel("./check_instance.xlsx")
'''
'''
with open("./temp_instance.jsonl","a",encoding="UTF-8") as f:
    for line in data:
        json.dump(line,f)
        f.write("\n")
'''
fail_data=[]
with open("../data/instaces/instances_v2.jsonl", "r", encoding="UTF-8") as f:
    for line in f:
        json_data = json.loads(line)
        machines = json_data["machines"]
        jobs = json_data["jobs"]
        num_machine = json_data['problem']['machines']
        num_job = json_data['problem']['jobs']
        if num_machine != len(machines) or num_job != len(jobs):
            fail_data.append(json_data)
print(len(fail_data))
