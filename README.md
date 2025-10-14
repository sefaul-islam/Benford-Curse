<div align=center>

# **[Neurips 2025]** Benford's Curse: Tracing Digit Bias to Numerical Hallucination in LLMs

</div>


## Getting started

### Environment Setup

1. clone the repository

```bash
git clone https://github.com/shamy28/Benford-Curse.git && cd Benford-Curse
```

2. install dependencies

```bash
pip install -r requirements.txt
```


## Datasets


The datasets used in this paper are located in the `Datasets/` directory. The directory contains the following files and directory:

### Identification Task

Both files contain 100 numerical sequences, each with the same configuration except for the last term. 

- `identification_lastbig.csv`
- `identification_lastsmall.csv`

### Digit Bias Benchmark
 Seven tasks on digit bias.


## Neuron_Bias
A compressed version of the biased neurons is provided for convenience. Users are advised to decompress the archive prior to usage.

## generation
The generation code for both the original and the pruned models is provided in the `generation/` directory.

## Check
To check the result of the generation content, please use the code at `Check\`. We suggest using an LLMs to extract the answer first.

## Probing 
We provide the original code for extracting digit selectivity of individual neurons in this directory. A complete version of the probing code will be released upon publication.
 

## Running the Model


Before running the code, please download the LLMs. You can get access to all the models in this paper at https://huggingface.co/.

To run the model for a specified task, use the following command:

```bash
python model_generation_pruned.py --model_name llama27b --task evaluate --output_path "~/your_path"
```


## Citation

```
@article{shao2025benford,
  title={Benford's Curse: Tracing Digit Bias to Numerical Hallucination in LLMs},
  author={Shao, Jiandong and Lu, Yao and Yang, Jianfei},
  journal={arXiv preprint arXiv:2506.01734},
  year={2025}
}
```
