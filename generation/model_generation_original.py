import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from uilts import read_arthmetics, write_result
import argparse

parser.add_argument("--model_name", type=str, required=True, help="model")
parser.add_argument("--task", type=str, required=True, help="task")
parser.add_argument("--output_path", type=str, required=True, help="output_path")
model_name = args.model_name
task = args.task
output_path=args.output_path
model_path=f"~/llm/{model_name}"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="cuda:2",
                                             attn_implementation="eager")
model.eval()

questions, answers = read_arthmetics(
    f"~/Datasets/{task}.txt")
output_path = "~/Your_path"
for frame in range(len(questions)):
    prompt = questions[frame]
    answer = answers[frame]
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    input_ids = tokenizer([text], return_tensors="pt").to(model.device)

    # Generation parameters
    max_length = 1024
    eos_token_id = tokenizer.eos_token_id

    # Greedy generation

    with torch.no_grad():
        for _ in range(max_length):

            outputs = model(**input_ids)
            logits = outputs.logits
            next_token_logits = logits[:, -1, :]
            next_token = torch.argmax(next_token_logits, dim=-1).item()
            token = tokenizer.convert_ids_to_tokens(next_token)
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
