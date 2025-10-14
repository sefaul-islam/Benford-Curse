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
    last_equation = lines[-1]
    pattern = r"-?(?:\d[\d,]*)(?:\.\d+)?"
    numbers = re.findall(pattern, last_equation)

    if not numbers:
        return False

    cleaned_numbers = []
    for num_str in numbers:

        cleaned_num = float(num_str.replace(',', ''))
        cleaned_numbers.append(cleaned_num)

    result = cleaned_numbers[-1]
    result = format_number(result)
    result_str = str(result)

    print(result)
    print(result==answer)

    return result_str,answer_str

def format_number(num):
    if int(num) == num:
        return int(num)
    else:
        return num
if __name__ == '__main__':
    blocks = split_answer_blocks("~/reponse.txt")
    cnt=0
    cnt_true=0
    loss=[]
    res_list=[0]*10
    ans_list=[0]*10
    cnt_flase=0
    cnt_flase_list=[]
    res_strange=[]

    for idx, block in enumerate(blocks, start=1):
        flag=0

        print(f"答案块 {idx}：")
        print(block)
        print("=" * 40)
        if check_value(block)==False:
            cnt_flase=cnt_flase+1
            cnt_flase_list.append(idx)
            continue
        res,ans=check_value(block)

        for j in range(10):
            if res.count(str(j))>2:
                res_strange.append([res,idx])
                flag=1
                break
        if flag==1:
            continue
        
        for i in range(0,10):
            res_list[i]=res.count(str(i))+res_list[i]
            ans_list[i]=ans.count(str(i))+ans_list[i]
    print(cnt)
    print(cnt_true)
    print(res_list)
    res_list=[i/sum(res_list) for i in res_list]
    ans_list=[i/sum(ans_list) for i in ans_list]
    res_list_round = [round(x, 4) for x in res_list]
    ans_list_round = [round(x, 4) for x in ans_list]
    print("res_list:",res_list_round)
    print("ans_list:",ans_list_round)
    print("cnt_flase:",cnt_flase)
    print("res_strange:",res_strange)
    print("cnt_flase_list:",cnt_flase_list)
    print(len(res_strange))
