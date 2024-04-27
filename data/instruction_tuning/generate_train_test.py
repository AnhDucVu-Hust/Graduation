import json
import random
import os


def extract_from_problem(problem):
  machines = [f'Machine {i}' for i in range(problem['machines'])]
  if 'optimum' in problem.keys():
    optimum = problem['optimum']
  else:
    optimum = None
  operation_matrix = []
  for job in problem['details']:
    tasks = job['tasks']
    operation = [(task['machine_id'], task['processing_time']) for task in tasks]
    operation_matrix.append(operation)
  return f"""Operation matrix: {operation_matrix}
"""
def split_json_files(data_dir, train_file, test_file,train_ratio=0.8):
  """
  Splits JSON files in a directory into train and test sets based on file count.

  Args:
    data_dir: Path to the directory containing JSON files (string).
    train_file: Path to the output train file (string).
    test_file: Path to the output test file (string).
    num_files: Total number of JSON files (default: 10).
    train_ratio: Ratio of files for the training set (default: 0.8).
  """

  all_files = [os.path.join(data_dir, filename) for filename in os.listdir(data_dir) if filename.endswith(".json")]
  random.shuffle(all_files)
  train_count = int(len(all_files) * train_ratio)
  train_files = all_files[:train_count]
  test_files = all_files[train_count:]
  instruction = """Act as an genetic computation program, you will help people to solve the problem with genetic algorithm.

I will give you a Job Shop Scheduling Problem (JSSP) and  10 solutions for it.
The solution will be encoded as a sequence of jobs, the ith occurrence of the job corresponding to the ith operation. Create the next population for me.
Each solution will be put between <solution> and </solution>
"""
  train_data = []
  for filepath in train_files:
    with open(filepath, "r") as f:
      name = filepath.split("_")[-1].replace(".json","")
      problem = extract_from_problem(name2data[name])
      data = json.load(f)
      for x in data:
        x['instruction'] = instruction + problem
      train_data.extend(data)

  test_data = []
  for filepath in test_files:
    with open(filepath, "r") as f:
      name = filepath.split("_")[-1].replace(".json", "")
      problem = extract_from_problem(name2data[name])
      data = json.load(f)
      for x in data:
        x['instruction'] = instruction + problem
      test_data.extend(data)

  with open(train_file, "a") as f:
    for data in train_data:
      json.dump(data, f, ensure_ascii=False)
      f.write("\n")

  with open(test_file, "w") as f:
    for data in test_data:
      json.dump(data, f, ensure_ascii=False)
      f.write("\n")
data_dir = "./"
train_file = "./train.json"
test_file = "./test.json"
with open("../jssp/jssp.json", "r", encoding="UTF-8") as f:
  data = json.load(f)
name2data = {t['name']:t for t in data}
split_json_files(data_dir,train_file,test_file)
