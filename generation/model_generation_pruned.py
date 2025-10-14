import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from uilts import read_arthmetics, write_result
from get_neuron import masktop1neuron
from types import MethodType
import argparse
parser.add_argument("--model_name", type=str, required=True, help="model")
parser.add_argument("--task", type=str, required=True, help="task")
parser.add_argument("--output_path", type=str, required=True, help="output_path")
model_name = args.model_name
task = args.task
output_path=args.output_path
model_path=f"~/llm/{model_name}"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="cuda:0",
                                             attn_implementation="eager")
model.eval()
mask_path = torch.load(
    f"~/Neuron_bias/{model_name}_eachneurondsc.npy",
    weights_only=True, map_location=model.device)
mask_path = mask_path[:, :, 1]
mask = masktop1neuron(mask_path)
num_layers = model.config.num_hidden_layers  # 32
intermediate_size = model.config.intermediate_size  # 14336


def factory(idx, mask):
    def custom_forward(self, x):
        gate_act = self.act_fn(self.gate_proj(x))
        gate_act[:, -1, :] = gate_act[:, -1, :] * mask[idx]
        down_proj = self.down_proj(gate_act * self.up_proj(x))
        return down_proj
    return custom_forward


original_mlp_forward = [None for _ in range(num_layers)]
for i in range(num_layers):
    layer = model.model.layers[i]
    original_mlp_forward[i] = layer.mlp.forward

questions, answers = read_arthmetics(
    "~/Datasets/sequence_next_term.txt")
for frame in range(len(questions)):
    prompt = questions[frame]
    answer = answers[frame]
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    input_ids = tokenizer([text], return_tensors="pt").to(model.device)
    max_length = 1024
    eos_token_id = tokenizer.eos_token_id
    with torch.no_grad():
        for _ in range(max_length):
            outputs = model(**input_ids)
            logits = outputs.logits
            next_token_logits = logits[:, -1, :]
            next_token = torch.argmax(next_token_logits, dim=-1).item()
            token = tokenizer.convert_ids_to_tokens(next_token)
            token = tokenizer.convert_ids_to_tokens(next_token)
            if token >= "0" and token <= "9":
                for i in range(num_layers):
                    layer = model.model.layers[i]
                    mlp = layer.mlp
                    mlp.forward = MethodType(factory(i, mask=mask), mlp)
                outputs = model(**input_ids)
                logits = outputs.logits
                next_token_logits = logits[:, -1, :]
                next_token = torch.argmax(next_token_logits, dim=-1).item()
                for i in range(num_layers):
                    layer = model.model.layers[i]
                    layer.mlp.forward = original_mlp_forward[i]
            next_token_tensor = torch.tensor([[next_token]], device=input_ids['input_ids'].device)
            input_ids['input_ids'] = torch.cat([input_ids['input_ids'], next_token_tensor], dim=-1)

            # Update attention mask if present
            if 'attention_mask' in input_ids:
                input_ids['attention_mask'] = torch.cat(
                    [input_ids['attention_mask'], torch.ones_like(next_token_tensor)], dim=-1
                )

            if next_token == eos_token_id:
                break
    # Decode output
    generated_text = tokenizer.decode(input_ids['input_ids'][0], skip_special_tokens=True)
    # print("Generated Text:", generated_text)
    write_result(frame, output_path, generated_text, answer)
    print(f"{frame + 1}/{len(questions)}")
