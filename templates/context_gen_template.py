template_1 = '''
The job shop scheduling problem (JSSP), also known as the job-shop problem, is a common optimization problem encountered in various industries like manufacturing, construction, and healthcare. It involves scheduling multiple jobs that require processing on shared resources (machines) in a specific order. 

The goal is to find the optimal schedule that minimizes a specific objective, typically the makespan.

Here's a breakdown of the key aspects:
Jobs: Each job consists of a sequence of tasks that need to be completed in a specific order.

Machines: There are a limited number of machines available, and each task requires a specific machine for processing.

A machine can only process one task at a time, meaning no two tasks can be processed on the same machine simultaneously.
Create for me some real-life contexts of Job Shop Scheduling Problem:\n

'''
prompt_instance = '''
##Context: {context}
JSP Parameters:
## The number of machines: {m}
## The number of jobs: {j}
'''
prompt_instance_v2 = '''
# Context: {context}
# Processing time for each job:
{processing_time}
'''
template_instances =[
    {
      "role": "system",
      "content": "The job shop scheduling problem (JSSP), also known as the job-shop problem, is a common optimization problem encountered in various industries like manufacturing, construction, and healthcare. It involves scheduling multiple jobs that require processing on shared resources (machines) in a specific order. \n\nThe goal is to find the optimal schedule that minimizes a specific objective, typically the makespan.\n\nHere's a breakdown of the key aspects:\nJobs: Each job consists of a sequence of tasks that need to be completed in a specific order.\n\nMachines: There are a limited number of machines available.\n\nEach job have multiple of tasks and each task requires a specific machine for processing with processing times. and the order of the jobs must be in the correct order (The lower sequence number job must be executed before the higher sequence number job)\n\nEach job is assigned to one machine, and the order of the jobs must be in the correct order. The lower sequence number job must be executed before the higher sequence number job. We will represent the above information with a 2-dimensional matrix. Each row of the matrix will contain information about jobs, in which each job will be a couple (machine code, execution time).\n\nA machine can only process one task at a time, meaning no two tasks can be processed on the same machine simultaneously.\n\nFrom the context and parameters I provide (number of job, number of machines), you should create the real-life jobs and machines. \nYour response will in form\n\"\n#Machines\n(machines' name, each machine in a line)\n#Jobs\n(jobs'name, each job in a line). Remember to check that there are enough jobs and machines, if not, complete it. \n\"\nExample:\nUser:\n##Context: A construction company needs to schedule jobs for various tradespeople with different skills and equipment requirements. the goal is to minimize the total time it takes to complete all jobs.\nJSP Parameters:\n## The number of machine: 5\n## The number of job: 15\n\nAssistant:\n#Machines\nExcavator\nCrane\nConcrete Mixer\nScaffolding\nDump Truck\n\n#Jobs\nLaying Foundation\nBuilding Walls\nInstalling Roof\nPainting Exterior\nLandscaping\n\n"
    },
    {
      "role": "user",
      "content": ''
    }
  ]
template_instances_v2 =[
    {
      "role": "system",
      "content": "The job shop scheduling problem (JSSP), also known as the job-shop problem, is a common optimization problem encountered in various industries like manufacturing, construction, and healthcare. It involves scheduling multiple jobs that require processing on shared resources (machines) in a specific order. \\n\\nThe goal is to find the optimal schedule that minimizes a specific objective, typically the makespan\n  \nFrom the context, creatively make it to a specific and comprehensive description. Your response only has the paragraph and nothing else\n\nExample:\n# Context: A construction company needs to schedule various tasks for different projects requiring multiple crews and equipment. optimizing the schedule minimizes job completion time and maximizes resource utilization.\n\nA construction company named \"Builders United\" needs to schedule jobs for various projects with different skills and equipment requirements to minimize the total time it takes to complete all jobs.\n\n\n"
    },
    {
      "role": "user",
      "content": ''
    }
  ]

templete_generate_solution = [
    {
      "role": "system",
      "content": "This is an example of a job shop scheduling problem, you are a virtual assistant who help me by giving a schedule directly for it. Remember the operation must be done in sequence, the operation with lower id must be done earlier.  You should give me a good schedule, which make the makespan (the time to processing all) is minimum\n\nThe schedule will be form like a python list of job_id, each id will appear as many times as its operation number \n\n"
    },
    {
      "role": "user",
      "content": ""    }
  ]