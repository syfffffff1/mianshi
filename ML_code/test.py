import json
import re
import time
# 文件路径
file_path = 'data/test.json'

# 打开文件并加载其内容
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
# 存储匹配的文本
i = 0
qa_pairs = []

begin_time = time.time()
for entry in data:
    input_text = entry['input']
    orgin_id = entry['id']
    options = entry['options']
    gold_index = entry['gold_index']
    class_id = entry['class_id']

    # 获得最后一个问题
    start_index = input_text.rfind("Does the news headline")
    end_index = input_text.find("?", start_index)
    last_question = input_text[start_index:end_index+1]  # 从 start_index 到文本末尾
    last_answer = options[gold_index]
    # 匹配从 "Does the news headline" 开始到下一个 "\n\n" 之间的文本
    matches = re.findall(r'Does the news headline.*?\n\n', input_text, re.DOTALL)
    for match in matches:

        # 提取 "Does the news headline" 到 "\n\n" 之间的文本
        start = match.find('Does the news headline')
        end = match.find('\n\n')
        extracted_text = match[start:end]
        question_mark = match.find('?')
        question = extracted_text[:question_mark+1]
        answer_mark = extracted_text.rfind(' ')
        answer = extracted_text[answer_mark+1:]
        # 创建一个字典来存储每个问题-答案对的信息
        qa_dict = {
            "id": i,  # 使用id和索引作为唯一标识符
            "Question": question,
            "Answer": answer,
            "Origin_id": orgin_id,  # 添加选项信息
            "class_id": class_id
        }
        qa_pairs.append(qa_dict)
        i += 1
    
    qa_dict = {
            "id": i,  # 使用id和索引作为唯一标识符
            "Question": last_question,
            "Answer": last_answer,
            "Origin_id": orgin_id,  # 添加选项信息
            "class_id": class_id
        }
    qa_pairs.append(qa_dict)
    i += 1
# for text in qa_pairs:
#     print(text)

# 最后，将qa_pairs列表写入JSON文件
output_file_path = 'data/output.json'  # 设定输出文件路径
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(qa_pairs, output_file, indent=4, ensure_ascii=False)  # 保存为JSON格式，设置缩进便于阅读
last_time = time.time()

times = last_time - begin_time
print(times)