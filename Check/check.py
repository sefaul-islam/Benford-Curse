import re


def check_answer_in_block(block):

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

    rest_text = "\n".join(lines[1:])
    

    return answer_str in rest_text

