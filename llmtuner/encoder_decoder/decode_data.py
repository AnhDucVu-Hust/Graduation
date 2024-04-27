import numpy as np
import random
num_job = 10
num_machines = 10
sol = [list(np.random.permutation(num_job)) for _ in range(num_machines)]
T = [list(np.random.permutation(num_machines)) for _ in range(num_job)]
processìng_time = [[np.random.randint(0,15) for _ in range(num_machines)] for _ in range(num_job)]
print(sol)
j=0
i=0
queue = []
operation = [0 for _ in range(num_job)]
end_time = [0 for _ in range(num_job)]
machine_time = [0 for _ in range(num_machines)]
def check(job,machine):
    if machine != T[job][operation[job]]:
        return False
    return True
def process(job,machine):

while i < len(num_job):
    while j<len(num_machines):
        job_check = sol[j][i]
        if check(job_check,j):
            queue.insert(0,{'job':i,'machine':j})
        else:



