import json
def extract_from_problem(problem):
    #machines = [f'Machine {i}' for i in range(problem['machines'])]
    if 'optimum' in problem.keys():
        optimum = problem['optimum']
    else:
        optimum = None
    operation_matrix = []
    for job in problem['details']:
        tasks = job['tasks']
        operation = [(task['machine_id'],task['processing_time']) for task in tasks]
        operation_matrix.append(operation)
    return operation_matrix,optimum
instruction = "From the Job Shop Scheduling Problem use case, let's parse it into a task specification (machines list, jobs list and operation matrix) so the coder can code from it "
with open("../data/instaces/instances_full_v2.jsonl","r",encoding="UTF-8") as f:
    text_jssp = [json.loads(line) for line in f]
with open("../data/instaces/instances_v2.jsonl","r",encoding="UTF-8") as f:
    params = [json.loads(line) for line in f]
text2param=[]
for instance in text_jssp:
    text = instance['content']
    id = instance['index']
    param = params[id]
    machines = param["machines"]
    jobs = param["jobs"]
    problem = param["problem"]
    operation_matrix,optimum = extract_from_problem(problem)
    declare = f"""# Machine: {machines}
# Job: {jobs}
# Operation matrix: {operation_matrix}
"""
    text2param.append({'instruction':instruction,'input':text,"output":declare})
with open("../data/instaces/text2param.jsonl","a",encoding="UTF-8") as f:
    for instance in text2param:
        json.dump(instance,f,ensure_ascii=False)
        f.write("\n")
