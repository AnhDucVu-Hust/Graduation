from collections import defaultdict


class Genome:
    def __init__(self,problem,solution):
        self.problem = problem
        self.solution = solution
        self.get_value()
    def get_value(self):
        count_job = defaultdict(int)
        machine_time = {k: 0 for k in range(len(self.problem.machines))}
        job_process_time = defaultdict(int)
        machine_str  = [[] for _ in range(len(self.problem.machines))]
        for job_id in self.solution:
            operation_id = count_job[job_id]
            temp_op = self.problem.jobs[job_id].operation[operation_id]
            machine = temp_op.machine.machine_id
            time_consume = temp_op.time_consume
            if machine_time[machine] >= job_process_time[job_id]:
                machine_time[machine] += time_consume
            else:
                gap =job_process_time[job_id]-machine_time[machine]
                machine_time[machine] = job_process_time[job_id] + time_consume
                for _ in range(gap):
                    machine_str[machine].append(' ')
            for _ in range(time_consume):
                machine_str[machine].append(job_id)
            job_process_time[job_id] =machine_time[machine]
            count_job[job_id] += 1
        self.score = max(machine_time.values())
        self.machine_str = [''.join([str(x) for x in machine_string]) for machine_string in machine_str]
        self.machine_time = machine_time
    def print_scheduling(self):
        print("Makespan:", self.score)
        for i,machine in enumerate(self.machine_str):
            print(f"## {self.problem.machines[i].name:15}|{machine}\n")


