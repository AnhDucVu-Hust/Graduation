import json
from GA.params import Problem
from GA.genome import  Genome
from GA.solver import GA
with open("./jssp.json","r",encoding="UTF-8") as f:
    data = json.load(f)

def extract_from_problem(problem):
    machines = [f'Machine {i}' for i in range(problem['machines'])]
    if 'optimum' in problem.keys():
        optimum = problem['optimum']
    else:
        optimum = None
    operation_matrix = []
    for job in problem['details']:
        tasks = job['tasks']
        operation = [(task['machine_id'],task['processing_time']) for task in tasks]
        operation_matrix.append(operation)
    return machines,operation_matrix,optimum
machines,operation_matrix,optimum = extract_from_problem(data[1])
prob = Problem(machines,operation_matrix,optimum=optimum)
prob.print_infor()
#ga = GA(problem=prob)
import time
#start_time = time.time()
#ga.solve(population_size=32,num_steps=1500)
#print("Solve in: ",time.time()-start_time)
#print(prob.print_infor())
print(prob.operation_matrix)