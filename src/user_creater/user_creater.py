"""
程序入口：
    1. 读取Json文件
    2. AI生成具体用户（每次生成一个）
    3. 文件保存到指定文件夹（以JSON文件命名，标号）
作用：
    根据模版生成具体的用户画像
"""

import json
import os
import glob
import sys

from openai import OpenAI

# sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
import config

# user模版 文件夹路径1
file_path_1 = "Json_User/User"
# user模版 文件夹路径2
file_path_2 = "2_travel"
# file_path_2 = "3_entertainment"
# file_path_2 = "4_shoppingPreferences"
# file_path_2 = "5_edu"
# file_path_2 = "6_health"
# JSON 文件名（用作存储文件夹）
file_name = "12_11"

save_path = "Json_User/result"

# JSON 文件路径+文件名（最终路径）
file_name_final = file_path_1 + "/" + file_path_2 + "/" + file_name + ".json"

os.environ["HTTP_PROXY"] = config.HTTP_PROXY
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL,
)
GlobalModel = config.GLOBAL_MODEL

system_content = [
    """你是一名用户信息填写者，你将会收到一份JSON模版，要求你根据模版中的描述填写信息。你需要遵循以下规则：
1. 直接返回JSON数据：请直接返回填充好的JSON数据，不要使用Markdown格式或其他任何格式。
2. 发散思维，个性化填写：所填写的信息应该合理、丰富且多样，体现每一个用户的个性化。避免生成过于普通或常见的信息，确保每个用户画像都是独特的。
3. 避免与参考值相同：所填写的信息不应该与模板中的 referenceValue 相同，确保每个属性的值都是唯一的。
4. 填满所有属性：模板中的每个属性都必须填写，不能有遗漏。
5. 生成一个完整的用户画像：每次生成一个完整的用户画像，确保所有属性的值都符合上述要求。
请根据以上规则，填写并返回完整的JSON数据。
"""
]
user_message = "JSON模版如下所示："


class Agent:
    def __init__(self):
        self.messages = []
        self.messages.append({"role": "system", "content": system_content[0]})

    def interact(self, message):
        # 将用户消息传递到消息列表
        self.messages.append({"role": "user", "content": message})

        # 调用OpenAI AI 获取响应
        response = client.chat.completions.create(
            model=GlobalModel, messages=self.messages, temperature=1.5
        )

        # 获取并返回 AI 的响应
        ai_response = response.choices[0].message
        self.messages.append(ai_response)
        return ai_response.content


def json_message():
    # 读取 JSON 文件
    with open(file_name_final, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 遍历数据并生成消息
    json_message = [json_data]
    return json_message


def json_save(ai_response):
    # 要保存的文件夹
    save_path_package = save_path + "/" + file_path_2 + "/" + file_name
    # 确保文件夹存在，不存在则新建
    if not os.path.exists(save_path_package):
        os.makedirs(save_path_package)

    # 使用 glob 匹配所有 .json 文件
    json_files = glob.glob(save_path_package + "/*.json")

    # 提取文件名中的数字部分，并找到最大的数字
    max_number = 0
    for json_file_path in json_files:
        json_file_name = os.path.basename(json_file_path)

        number = int(json_file_name.split(".")[0])
        if number > max_number:
            max_number = number

    # 将最大数字加 1，作为新文件的文件名
    new_file_name = str(max_number + 1) + ".json"
    new_file_path = os.path.join(save_path_package, new_file_name)

    json_ai_response = json.loads(ai_response)
    with open(new_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_ai_response, json_file, ensure_ascii=False, indent=4)


def user_creater():
    # 创建一个 Agent 实例
    agent = Agent()
    json_data = json_message()
    json_data_message = json.dumps(json_data, indent=4)
    combine_message = f"{user_message}\n{json_data_message}"
    print(combine_message)
    ai_response = agent.interact(combine_message)
    print(ai_response)
    json_save(ai_response)
    print("Done")


def main():
    # n 生成用户的数量
    n = 5
    for i in range(n):
        user_creater()


if __name__ == "__main__":
    main()
