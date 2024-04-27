from genome import *
from params import *
from solver import GA,PSO
import json
from params import extract_from_problem
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
with open("../data/jssp/jssp.json","r",encoding="UTF-8") as f:
    problems = json.load(f)



def gen_population(solver,problem,multi_step=False):
    instruction = "Act as an genetic computation program, you will help people to solve the problem with genetic algorithm.\n\nI will give you a Job Shop Scheduling Problem (JSSP) and  10 solutions for it.\n\nThe solution will be encoded as a sequence of jobs, the ith occurrence of the job corresponding to the ith operation.You need to generate 10 offspring solution for me. Each solution will be put between <solution> and </solution> \n Problem: {problem}\n"
    if len(problem.jobs)>15 or len(problem.machines)>15:
        return None
    if solver =="PSO":
        genetic = PSO(problem,population_size=10)
        genetic.solve(num_steps=250)
        populations = genetic.populations
        local_best = genetic.local_optimum
        print(len(local_best))
        print(len(populations))
    else:
        genetic = GA(problem, population_size=10)
        genetic.solve(num_steps=250)
        populations = genetic.populations

    populations_str = []
    best_now = 1000000000
    for id,population in enumerate(populations):
        if local_best[id] < best_now:
            population_str = '\n'.join([f"<solution>{sol}</solution>" for sol in population])
            populations_str.append({"iteration":id,'population':population_str,"best_optimum":local_best[id]})
            best_now = local_best[id]
    with open(f"../data/fine-tuning/{solver}_{problem.name}.json","w",encoding="UTF-8") as f:
        json.dump(populations_str,f,ensure_ascii=False)
    with open(f"../data/instruction_tuning/{solver}_{problem.name}.json","w",encoding="UTF-8") as f:
        instruction_tuning = [{"instruction":instruction.format(problem=problem.operation_matrix),"input":populations_str[i]['population'],"output":populations_str[i+1]['population']} for i in range(len(populations_str)-1)]
        json.dump(instruction_tuning,f,ensure_ascii=False)
    if multi_step==True:
        multi_step_instruction = "Act as an genetic computation program, you will help people to solve the problem with genetic algorithm.\n\nI will give you a Job Shop Scheduling Problem (JSSP) and  10 solutions for it.\n\nThe solution will be encoded as a sequence of jobs, the ith occurrence of the job corresponding to the ith operation.You need to generate 1 offspring solution for me. Each solution will be put between <solution> and </solution> \n Problem: {problem}\n"
        multi_step= []
        for id in range(len(populations_str)-1):
            pop_now = populations_str[id]['population']
            pop_now += "\n# Offspring solution:"
            pop_next = populations_str[id+1]['population'].split("\n")
            for sol in pop_next:
                multi_step.append({'instruction':multi_step_instruction.format(problem=problem.operation_matrix),"input":pop_now,"output":sol})
                pop_now += sol+"\n"
        with open(f"../data/multi_step_instruction_tuning/{solver}_{problem.name}.json","w",encoding="UTF-8") as f:
            json.dump(multi_step,f,ensure_ascii=False)


    return populations_str
for problem in problems:
    gen_population("PSO",extract_from_problem(problem),multi_step=True)
