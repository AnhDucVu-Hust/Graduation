import json
import os
from params import extract_from_problem,Problem
from genome import Genome
with open("../data/jssp/jssp.json") as f:
    problems = json.load(f)
problems = {problem['name']:extract_from_problem(problem=problem) for problem in problems}
solution_file = os.listdir("../solution/")
solutions = {}
for file in solution_file:
    if file.endswith(".txt"):
        with open(f"../solution/{file}","r") as f:
            name = file.split(".")[0]
            data = f.readlines()
            solutions[name] = []
            for line in data:
                solutions[name].append(list(map(int,line.replace('<solution>','').replace('</solution>','').split(","))))
for name,solutions in solutions.items():
    problem = problems[name]
    scores = []
    optimum = problem.optimum
    for solution in solutions:
        x = Genome(problem,solution)
        scores.append(x.score)

    print(f"Name:{problem.name}, score:{min(scores)}, optimum value: {optimum}, metric:{optimum/min(scores)}")