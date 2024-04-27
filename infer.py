from transformers import AutoModelForCausalLM,AutoTokenizer
from data.jssp.extract import extract_from_problem
import json
with open("./data/jssp/jssp.json","r",encoding="UTF-8") as f:
    data = json.load(f)
data_dict = {t['name']:t for t in data}
class Inference:
    def __init__(self,args):
        self.args = args
        model_name = self.args.model_name
        problem = self.args.problem
        self.instruction = self.args.instruction
        self.optimum_matrix = extract_from_problem(data_dict[problem])
        if model_name != "gpt" or model_name != "gemini":
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.num_step =self.args.num_step
        self.generation_config = self.args.generation_config
        self.len_job = len(self.optimum_matrix)
        self.len_machine = len(self.)
    def run(self):
        if self.args.model == "gpt":
            messages = [{'role':'system','content':self.instruction+str(self.optimum_matrix)},{'role':'user','content':''}]

    def run_local_model(self):
        pass

