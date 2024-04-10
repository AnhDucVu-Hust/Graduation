from genome import *
from params import *
from solver import GA,PSO
import json
#provide machines name, operation matrix (jobs x machines x2),jobs_name
machines_name = ['Cut','Spray','Print']
operation_matrix = [[(0,1),(1,2),(2,3)],
                   [(1,2),(0,3),(2,4)],
                   [(2,2),(1,3),(0,3)]]
solution = [2,2,0,1,2,1,1,0,0]
jobs_name = ["Job 1","Job 2","Job 3"]
problem = Problem(name="NO",operation_matrix=operation_matrix)
problem.print_infor()
genome = Genome(problem,solution=solution)
genome.print_scheduling()
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
    #print(operation_matrix)
    return Problem(name = problem["name"],operation_matrix=operation_matrix,optimum=optimum)
with open("../data/jssp/jssp.json","r",encoding="UTF-8") as f:
    problems = json.load(f)

def gen_population(solver,problem):
    if solver =="PSO":
        genetic = PSO(problem,population_size=16)
        genetic.solve(num_steps=250)
        populations = genetic.populations
    else:
        genetic = GA(problem, population_size=16)
        genetic.solve(num_steps=250)
        populations = genetic.populations
    populations_str = []
    for id,population in enumerate(populations):
        population_str = '\n'.join([f"<solution>{sol}</population>" for sol in population])
        populations_str.append({"iteration":id,'population':population_str})

    with open(f"../data/fine-tuning/{solver}_{problem.name}.json","w",encoding="UTF-8") as f:
        json.dump(populations_str,f,ensure_ascii=False)
    print(problem.optimum)
    return populations_str
for problem in problems:
    gen_population("PSO",extract_from_problem(problem))
