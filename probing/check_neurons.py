import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from tqdm import tqdm
from collections import defaultdict
import numpy as np


model_name="your_model_name"
model_path=f"~/llm/{model_name}"

last = [0 for _ in range(10)]

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    device_map="cuda:2"
)
model.eval()


num_layers = model.config.num_hidden_layers
intermediate_size = model.config.intermediate_size
vocab_size = model.config.vocab_size
hidden_size = model.config.hidden_size
dsc_list = np.zeros((10, num_layers, intermediate_size))

results = defaultdict(list)
text_tokens = [str(i) for i in range(10)]
token_ids = tokenizer.convert_tokens_to_ids(text_tokens)
for layer in range(num_layers):
    layer_module = model.model.layers[layer].mlp.down_proj


    weight_matrix = layer_module.weight.T.to(torch.bfloat16)  
    temp = []
    for inter in range(intermediate_size):

        with torch.no_grad():
            logits = model.lm_head(weight_matrix[inter])
        top_ids = torch.topk(logits, k=vocab_size, dim=-1).indices.squeeze().tolist()
        num_rank = []
        for token_id in token_ids:
            rank = top_ids.index(token_id)
            num_rank.append(rank + 1)
        # dsc=[]
        for i in range(10):
            dsc_list[i, layer, inter] = sum(num_rank) / num_rank[i]
            # dsc.append(sum(num_rank)/num_rank[i])
np.save(
    f"~/{model_name}_eachneurondsc_10*{num_layers}*{intermediate_size}.npy",
    dsc_list)
