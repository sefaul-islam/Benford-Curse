import re
from check import check_answer_in_block
def split_answer_blocks(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()


    blocks = re.split(r'(?=^---------------\d+---------)', content, flags=re.MULTILINE)
    

    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks
def check_value(block):

    lines = block.splitlines()
    if not lines:
        return False

    header_line = lines[0]
    m = re.search(r'answer\s*is\s*:\s*(\[[^]]+\])', header_line, re.IGNORECASE)
    #print(m)
    if not m:
        return False

    answer_str = m.group(1)
    answer_str = answer_str.strip("[]")
    answer=float(answer_str)
    rest_text = "\n".join(lines[1:])
    last_equation=lines[-1]
    numbers = re.findall(r"-?\d+\.?\d*", last_equation)
    if len(numbers)==0:
        return "null"
    result=float(numbers[-1])
    result=format_number(result)
    result_str=str(result)
    print(result)
    print(result==answer)
    if abs(result)==abs(answer):
        return "true"
    else:
        return "wrong"

def format_number(num):
    if int(num) == num:
        return int(num)
    else:
        return num
if __name__ == '__main__':
    blocks = split_answer_blocks("~/reponse.txt")
    cnt=0
    cnt_true=[]
    loss=[]
    res_list=[0]*10
    ans_list=[0]*10
    cnt_flase=0
    cnt_flase_list=[]
    res_strange=[]

    for idx, block in enumerate(blocks, start=1):

        print(f"答案块 {idx}：")
        print(block)
        print("=" * 40)
        if check_value(block)=="null":
            cnt_flase=cnt_flase+1
            cnt_flase_list.append(idx)
            continue
        else:
            if check_value(block)=="true":

                cnt=cnt+1
                cnt_true.append(idx)

    print("cnt_true:",cnt)
    print("cnt_flase:",cnt_flase)
    print("true_list:",cnt_true)

