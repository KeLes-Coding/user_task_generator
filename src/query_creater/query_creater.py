import json
import os
import sys

from openai import OpenAI

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
import config

# query 文件夹路径1
query_file_path_1 = "query_message/query_template"
# query 文件夹路径2
query_file_path_2 = "2_travel"
# query 文件夹路径3
query_file_path_3 = "1_one_to_many"
# query 文件名
query_file_name = "1"

# query 模版文件路径（最终路径）
query_file_final = (
    query_file_path_1
    + "/"
    + query_file_path_2
    + "/"
    + query_file_path_3
    + "/"
    + query_file_name
    + ".txt"
)
# 用户画像 文件路径1
user_save_path_1 = "Json_User/result"
# 用户画像 文件路径2
user_save_path_2 = "2_travel"
# 用户画像 文件路径3
user_save_path_3 = "12_11"

# task 文件保存路径
task_save_path = (
    "query_message/result"
    + "/"
    + query_file_path_2
    + "/"
    + query_file_path_3
    + "/"
    + query_file_name
    + "/"
    + user_save_path_3
)


os.environ["HTTP_PROXY"] = config.HTTP_PROXY
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL,
)
GlobalModel = config.GLOBAL_MODEL

system_content = """
人设：你是一位为task模版进行信息填充的专家，你的任务是根据给定的task模版和用户画像，生成一个完整的task信息。
1. 直接返回JSON数据：请直接返回填充好的JSON数据，不要使用Markdown格式或其他任何格式。
2. task中参数应该严格与用户画像中对应的参数匹配
输出格式如下：
{
    "task": {
        "type": "string",
        "description": "Store the generated task.(English Version)"
    }
    "task-CN": {
        "type": "string",
        "description": "Store the generated task.(Chinese Version)"
    }
}
example:
{
    "task": "I'm planning to do outdoor adventure sports, which day is it? I wonder what the weather will be like in Sydney next weekend? My phone number is 18899908765, can you help me plan it?Depending on the weather conditions, please help me recommend some suitable activities first.Let's check the flight ticket from Beijing to Sydney that day.What are some of Sydney's most famous specialties? At 5:15 p.m., I was able to book a Mediterranean-style restaurant on the Champs-Elysées that I frequented, and I needed a quiet room.Four days later, I was able to book a Sheraton hotel on the Champs-Elysées that I liked to go to, the room was an executive room, and I asked for a quiet room."
    "task-CN": "我计划进行户外冒险运动，今天是哪一天？我想知道悉尼下个周末的天气怎么样？我的手机号是18899908765，你能帮我计划一下吗？根据天气情况，请先帮我推荐一些合适的活动吧。再查一下那天从北京去悉尼的飞机票吧。悉尼有哪些出名的特产？下午5:15帮我在香榭丽舍大街预定一个我常去的地中海风情餐厅，需要安静的房间。四天后帮我在香榭丽舍大街预定一家我最喜欢去的喜来登大酒店，房间是行政房，要求需要安静的房间。"
}
"""


class Agent:
    def __init__(self):
        self.messages = []
        self.messages.append({"role": "system", "content": system_content})

    def interact(self, user_template, task_template):
        # 将用户信息传递到消息列表
        self.messages.append(
            {
                "role": "user",
                "content": f"用户画像为：\n{user_template}\ntask模版为：\n{task_template}",
            }
        )

        # 调用OpenAI AI 获取响应
        response = client.chat.completions.create(
            model=GlobalModel, messages=self.messages, temperature=0
        )

        # 获取并返回 AI 的响应
        ai_response = response.choices[0].message
        self.messages.append(ai_response)
        return ai_response.content


# 读取 query 模板文件
def query_template_message():
    with open(query_file_final, "r", encoding="utf-8") as file:
        content = file.read()
    return content


# task_json 文件保存
def json_save(ai_response, userID):
    # 要保存的文件夹task_save_path
    # 确保文件夹存在，否则新建
    if not os.path.exists(task_save_path):
        os.makedirs(task_save_path)

    # 提取文件名 userID
    new_file_name = str(userID) + ".json"
    new_file_path = os.path.join(task_save_path, new_file_name)

    json_ai_response = json.loads(ai_response)
    with open(new_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_ai_response, json_file, ensure_ascii=False, indent=4)


def main():
    query_template = query_template_message()
    print(query_template)

    # 获取 user 文件夹路径
    user_directory = os.path.join(user_save_path_1, user_save_path_2, user_save_path_3)

    # 获取 user 文件夹中的所有文件
    user_json_files = os.listdir(user_directory)

    # 获取 user文件夹 中所有文件
    for user_json_file in user_json_files:
        # 检查文件是否为 JSON 文件
        if user_json_file.endswith(".json"):
            # 获取用户编号
            user_ID = user_json_file.split(".")[0]

            # 构建完整的文件路径
            user_json_path = os.path.join(user_directory, user_json_file)

            # 打开并读取 JSON 文件
            with open(user_json_path, "r", encoding="utf-8") as f:
                user_json_data = json.load(f)

            # 遍历数据并生成消息
            json_message = [user_json_data]
            print(json_message)

            agent = Agent()
            ai_response = agent.interact(query_template, json_message)
            print(ai_response)
            json_save(ai_response, user_ID)


if __name__ == "__main__":
    main()
