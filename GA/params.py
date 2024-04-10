class Job:
    def __init__(self,name,operation):
        self.name=name
        self.operation=operation
    def print_operation(self):
        for i,op in enumerate(self.operation):
            print(f"Operation {i+1}, machine:{op.machine.name} , processing time:{op.time_consume}")

class Op:
    def __init__(self,machine,time_consume):
        self.machine = machine
        self.time_consume = time_consume
class Machine:
    def __init__(self,name,machine_id):
        self.name = name
        self.machine_id = machine_id
class Problem:
    def __init__(self,name,operation_matrix,machines=None,jobs_name=None, optimum=None):
        #self.machines_name = machines
        self.name = name
        if machines == None:
            len_machine = len(operation_matrix[0])
            self.machines = [Machine(name=f'Machine {i}', machine_id=i) for i in range(len_machine)]
        else:
            self.machines = [Machine(name=machines[i],machine_id=i) for i in range(len(machines))]
        self.operation_matrix = operation_matrix
        if jobs_name:
            self.jobs_name = jobs_name
        else:
            len_jobs =len(operation_matrix)
            self.jobs_name = [f'Job{i+1}' for i in range(len_jobs)]
        self.jobs=[]
        for id,job_ops in enumerate(operation_matrix):
            temp_ops = []
            for op in job_ops:
                machine_id = op[0]
                time_consume = op[1]
                op = Op(self.machines[machine_id],time_consume)
                temp_ops.append(op)
            self.jobs.append(Job(name=self.jobs_name[id],operation=temp_ops))
        self.optimum = optimum

    def print_infor(self,show_optimum=True):
        print("## Number of machines " + str(len(self.machines)))
        print("## Number of jobs " + str(len(self.jobs)))
        for job in self.jobs:
            print(f'# {job.name}')
            job.print_operation()
        if self.optimum and show_optimum:
            print("Optimum value: ",str(self.optimum))


