from params import Problem
from genome import Genome
import json
with open("../jssp/jssp.json", "r", encoding="UTF-8") as f:
  data = json.load(f)
name2data = {t['name']:t for t in data}
def parsing_solution(sol,problem:Problem):
    if sol.startswith("<solution>") != True:
        return None
    elif sol.endswith("</solution>") != True:
        return None
    else:
        sol = sol.replace("<solution>","").replace("</solution>","")
        sol = sol.split(",")
        if len(sol) != len(problem.machines)*len(problem.jobs):
            return None
        standard_list = []
        for _ in range(len(problem.machines)):
            standard_list.extend(range(len(problem.jobs)))
        if sorted(sol) != sorted(standard_list):
            return None
        return Genome(sol,problem)


