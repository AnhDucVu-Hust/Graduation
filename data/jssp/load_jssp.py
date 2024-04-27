import json
import re

with open('instances.json', 'r') as file:
    # Load the JSON data into a Python list of dictionaries
    datas = json.load(file)
data_remake = []
for data in datas:
    path = data['path']
    with open(path,'r') as f:
        lines = f.readlines()
        id=0
        for i,line in enumerate(lines):
            if re.match(r'^\d', line):
                id=i
                break
    lines=lines[id+1:]
    matrixs = []
    for i,line in enumerate(lines):
        matrix = []
        x = line.split()
        for j in range(int(len(x)/2)):
            machine=int(x[2*j])
            cost_time =  int(x[2*j+1])
            matrix.append({'machine_id':machine,'processing_time':cost_time})
        matrixs.append({'job_id':i,'tasks':matrix})
    jobs = data['jobs']
    machines = data['machines']
    name = data['name']
    optimum =data['optimum']
    data_remake.append({'name':name,'jobs':jobs,'machines':machines,'details':matrixs,'optimum':optimum})
with open('jssp.json',"w") as f:
    json.dump(data_remake,f)

