from GA.genome import *
from GA.params import *
from GA.solver import GA
#provide machines name, operation matrix (jobs x machines x2),jobs_name
machines_name = ['Cut','Spray','Print']
operation_matrix = [[(0,1),(1,2),(2,3)],
                   [(1,2),(0,3),(2,4)],
                   [(2,2),(1,3),(0,3)]]
problem = Problem(machines_name,operation_matrix)
problem.print_infor()
#genome.print_scheduling()
genetic = GA(problem)
genetic.solve(population_size=20,num_steps=20)
print(genetic.population)
def genetic_llm_generate(instance):
    machines = instance['machines']
    jobs = instance['jobs']
    problem = instance['problem']
    if len(machines) != problem['machines'] or len(jobs) != problem['jobs']:
        return None

