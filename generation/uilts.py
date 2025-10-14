import csv
import random
import torch
import json


def read_csv(output_file):
    quelist = []
    anslist = []
    querylist = ["What is the sum of the first and last terms of this sequence?",
                 "What is the sum of the sequence's starting and ending terms?",
                 "What is the sum of the sequence's first term and its last term?"]
    querylist2 = ["What is the result when the last term of the sequence is multiplied by two?",
                  "What is the outcome when the final term of the sequence is doubled?",
                  "What is the product of the sequence's last term and two?",
                  "What is the result of multiplying the sequence's last term by two?"
                  ]
    # output_file = "/home/jianfeiyang/jianfeiyang/shaojiandong/number_sense/dataset/random_numbers.csv"
    with open(output_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            random_number = random.randint(0, 3)
            numeric_row = [float(value) for value in row]
            # ans = round(numeric_row[0] + numeric_row[-1], 2)
            # ans=str(ans)
            ans = round(2 * numeric_row[-1], 2)
            ans = str(ans)
            sen = querylist2[random_number] + str(numeric_row)
            # sen="How many numbers are there in this list?"+str(numeric_row)
            # sen="What is the result when the last term of the sequence is multiplied by two?"+str(numeric_row)
            quelist.append(sen)
            anslist.append(ans)
    return quelist, anslist

def write_result(frame, output_path, output, answer):
    with open(output_path, 'a') as f:
        f.write(f"\n---------------{frame}---------answer is:[{answer}]-------\n")
        f.write(output)


def read_arthmetics(arthmetics_file):
    with open(arthmetics_file, "r") as f:
        lines = f.readlines()
    questions = []
    answers = []
    for line in lines:

        line = line.strip()

        last_space_index = line.rfind(" ")

        question = line[:last_space_index].strip()
        answer = line[last_space_index + 1:].strip()

        questions.append(question)
        answers.append(answer)
    return questions, answers







