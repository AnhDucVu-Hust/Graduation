import dataclasses

import torch

from transformers import PreTrainedModel, AutoModelForCausalLM, AutoTokenizer
from transformers.utils import ModelOutput
access_token = "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"

@dataclasses
class Output(ModelOutput):
    loss:float
    logits:torch.FloatTensor = None
class JSSP_LLM(torch.nn.Module):

    def __init__(self, path):
        super(JSSP_LLM, self).__init__()

        self.encode = AutoModelForCausalLM.from_pretrained(path, token=access_token)

        hidden_size = self.encode.config.hidden_size

        print(hidden_size)
        self.decoder = torch.nn.TransformerDecoder(

            decoder_layer=
            torch.nn.TransformerDecoderLayer(d_model=hidden_size, nhead=4),

            num_layers=6

        )
        self.embedding = self.encode.model.embed_tokens

        self.ln = self.encode.model.lm_head

    def get_mem(self, input_ids, attention_mask):
        outputs = self.llm(input_ids, attention_mask, output_hidden_states=True)

        memory = outputs.hidden_states[-1:]

        return memory

    def forward(self, input_ids, memory,labels = None):
        embeds = self.embedding(input_ids)
        outputs = self.decoder(embeds, memory)
        hidden_states = outputs[0]
        logits = self.ln(hidden_states)
        loss =None
        if labels!=None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss_fct = torch.nn.CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.encode.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)
        return Output(loss=loss,logit=logits)

device = "cuda"

model = JSSP_LLM("google/gemma-2b").to(device)

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b", token=access_token)

