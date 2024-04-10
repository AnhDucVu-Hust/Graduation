#from GA.params import *
from typing import List
import numpy as np
import random
from genome import Genome
from abc import ABC, abstractmethod
class Genetic_Algorithm(ABC):
    def __init__(self,problem,population_size):
        self.problem = problem
        self.jobs = problem.jobs  # List of Job, each job have name, list of operation have machine and time consuming
        self.machines = problem.machines  # List of machine have name and id
        self.populations = []
        self.population_size = population_size
    def solve(self,num_steps=100):
        initial_genomes = self.initial_solution(len(self.jobs), len(self.machines), self.population_size)
        # print(initial_genomes)
        population = [Genome(self.problem, genome) for genome in initial_genomes]
        population_str = [','.join([str(a) for a in x.solution]) for x in population]
        for id in range(len(population)):
            population_str[id] += "-" + str(population[id].score)
        self.populations.append(population_str)
        for _ in range(num_steps):
            self._step(population)
    @abstractmethod
    def _step(self,population):
        pass
    def initial_solution(self,num_job, num_machine, num_samples):
        datas = []
        for _ in range(num_samples):
            data = []
            for i in range(num_job):
                data.extend([i] * num_machine)
            random.shuffle(data)
            datas.append(data)
        return datas



class GA(Genetic_Algorithm):
    def __init__(self,problem,population_size):
        super().__init__(problem,population_size)
    def mutation(self,genome:Genome):
        genome = genome.solution.copy()
        index1,index2 = random.sample(range(len(genome)),2)
        genome[index1],genome[index2] = genome[index2], genome[index1]
        return Genome(self.problem,genome)
    def crossover(self,genome1:Genome,genome2:Genome):
        genome1 = genome1.solution.copy()
        genome2 = genome2.solution.copy()
        start = np.random.randint(0,len(genome1)-1)
        end = np.random.randint(start+1,len(genome1))
        sub_genome_1 = genome1[start:end]
        genome_1 = genome2.copy()
        for gene in sub_genome_1:
            index = [i for i,e in enumerate(genome_1) if e == gene]
            id_remove = random.sample(index,1)[0]
            del genome_1[id_remove]
        offstring_1 = genome_1[:start] + sub_genome_1 + genome_1[start:]
        sub_genome_2 = genome2[start:end]
        genome_2 = genome1.copy()
        for gene in sub_genome_2:
            index = [i for i, e in enumerate(genome_2) if e == gene]
            id_remove = random.sample(index, 1)[0]
            del genome_2[id_remove]
        offstring_2 = genome_2[:start] + sub_genome_2 + genome_2[start:]
        return (Genome(self.problem,offstring_1),Genome(self.problem,offstring_2))

    def tournament_selection(self,population,selection_size):
        selections = []
        for _ in range(selection_size):
            candidates = random.sample(population,2)
            candidate = min(candidates,key=lambda x:x.score)
            selections.append(candidate)
        return selections
    def _step(self,population):
        parents = self.tournament_selection(population, int(len(population)/ 2))
        children = []
        for i in range(0, len(parents), 2):
            child1, child2 = self.crossover(parents[i], parents[i + 1])
            children.extend([child1, child2])

        # Step 2: Mutation
        children = [self.mutation(child) for child in children]
        parents.extend(children)
        population = parents
        best_score = min(population, key=lambda x: x.score)
        print(best_score.score)
        population_str = [','.join([str(a) for a in x.solution]) for x in population]
        #for id in range(len(population)):
        #    population_str[id] += "-" + str(population[id].score)
        # population_str = '\n'.join([x for x in population_str])
        #print('\n'.join([x for x in population_str]))
        print("------------")
        self.populations.append(population_str)
class DE(Genetic_Algorithm):
    def __init__(self, problem,population_size):
        super().__init__(problem,population_size)
    def mutation(self,genome:Genome):
        candidates = [gen.solution.copy() for gen in self.population if gen != genome]
        random_candidate = np.random.choice(candidates,3,replace=False)
        return None
    def _step(self,population):
        return None
class PSO(Genetic_Algorithm):
    def __init__(self,problem,population_size,c1=0.2,c2=0.2,w=0.4):
        super().__init__(problem,population_size)
        self.c1=c1
        self.c2=c2
        self.w=w
        self.pbest = []
        self.gbest = None
    def mutation(self,genome_encoding):
        index1, index2 = random.sample(range(len(genome_encoding)), 2)
        genome_encoding[index1], genome_encoding[index2] = genome_encoding[index2], genome_encoding[index1]
        return genome_encoding
    def crossover(self,genome_enc1,genome_enc2):
        num_job = len(self.jobs)
        num_machine = len(self.machines)
        job_ids = list(range(num_job))
        sample_size = random.randint(1,num_job)
        random.shuffle(job_ids)
        sample = job_ids[:sample_size]
        temp = []
        genome_enc2 = [x for x in genome_enc2 if x not in sample]
        id_2 = 0
        for id,job in enumerate(genome_enc1):
            if job in sample:
                temp.append(job)
            else:
                temp.append(genome_enc2[id_2])
                id_2 +=1
        return temp
    def solve(self,num_steps=100):
        initial = self.initial_solution(len(self.jobs), len(self.machines), self.population_size)

        # print(initial_genomes)
        population = [Genome(self.problem, genome) for genome in initial]
        population_str = [','.join([str(a) for a in x.solution]) for x in population]
        self.pbest = population
        min_value = population[0]
        for x in population:
            if x.score < min_value.score:
                min_value = x
        self.gbest = min_value
        self.populations.append(population_str)
        for i in range(num_steps):
            new_pop = self._step(population)
            self.update_pbest_and_gbest(new_pop)
            population=new_pop


    def update_pbest_and_gbest(self,new_pop):
        for id,genome in enumerate(new_pop):
            if genome.score < self.pbest[id].score:
                self.pbest[id] = genome
            if genome.score < self.gbest.score:
                self.gbest = genome
        print("gbest value:", self.gbest.score)
    def _step(self,population):
        new_pop = []
        genome_enc = [genome.solution for genome in population]
        for id,x in enumerate(genome_enc):
            mut_genome = x
            if np.random.randn()> self.c1:
                mut_genome = self.mutation(x)
            pbest = self.pbest[id]
            if np.random.randn()> self.c2:
                mut_genome = self.crossover(mut_genome,pbest.solution)
            if np.random.randn() > self.w:
                mut_genome = self.crossover(mut_genome,self.gbest.solution)
            new_pop.append(mut_genome)
        population_str = [','.join([str(a) for a in x]) for x in new_pop]
        #print('\n'.join([x for x in population_str]))
        #print("------------")
        self.populations.append(population_str)
        return [Genome(self.problem,solution=x) for x in new_pop]


