- [x] 生成器-用户画像
- [x] 生成器-Task(用户画像)

# 模型参数在`src/config.py`中修改
```python
# qwen
API_KEY = ""
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
GLOBAL_MODEL = "qwen-plus"
```

# 生成器-用户画像
## 目录结构：
```
Json_User/
├── template/
├── User/
└── result/
```
* `template/`存放用户`元模版`（按照场景划分）
* `User/`存放用户画像模版
* `result/`存放具体用户画像
## 生成器
* 脚本位置：`src/user_creater/user_creater.py`
```python
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
```
只需修改
* `file_path_2`：场景
* `file_name`：用户画像名称
# 生成器-Task(根据用户画像生成)
## 目录结构
```
query_message/
├── query_template/
└── result/
```
* `query_template/`存放task模版
* `result/`存放生成的具体task
## 生成器
* 脚本位置：`src/query_creater/query_creater.py`
```python
# query 文件夹路径1
query_file_path_1 = "query_message/query_template"
# query 文件夹路径2
query_file_path_2 = "2_travel"
# query 文件夹路径3
query_file_path_3 = "1_one_to_many"
# query 文件名
query_file_name = "1"
```
只需修改
* `query_file_path_2`：场景
* `query_file_path_3`：task类型(一对多、多对一、多对多)
* `query_file_name`：task名称
```python
# 用户画像 文件路径1
user_save_path_1 = "Json_User/result"
# 用户画像 文件路径2
user_save_path_2 = "2_travel"
# 用户画像 文件路径3
user_save_path_3 = "12_11"
```
只需修改
* `user_save_path_2`：场景
* `user_save_path_3`：用户画像名称
