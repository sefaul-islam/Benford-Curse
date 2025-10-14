import torch


def masktop1neuron(tensor):

    flattened_tensor = tensor.flatten()

    k = max(1, int(flattened_tensor.numel() * 0.00005))

    top_k_values, _ = torch.topk(flattened_tensor, k)
    # print(top_k_values)
    threshold = top_k_values[-1]

    indices = (tensor >= threshold).nonzero(as_tuple=True)
    mask = torch.ones_like(tensor, dtype=torch.bool).to(tensor.device)
    mask[indices] = 0
    return mask






