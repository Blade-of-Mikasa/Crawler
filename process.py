import json
import os

# 输入 JSON 文件路径
input_file = r"D:\Crawler\posts.json"
output_file = r"D:\Crawler\data.txt"

# 从 JSON 文件加载数据并处理为指定格式
def process_json_file(input_file, output_file):
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"文件 {input_file} 不存在，请检查路径！")
        return
    
    # 加载 JSON 数据
    with open(input_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON 文件解析失败：{e}")
            return

    # 处理数据并保存到输出文件
    with open(output_file, "w", encoding="utf-8") as file:
        for item in data:
            user_id = item.get("user_id")
            user = item.get("user", {})
            nickname = user.get("nickname", "未知")
            name = item.get("name", "无标题")
            
            file.write(f"user_id: {user_id}:\n")
            file.write(f"    nickname: \"{nickname}\"\n")
            file.write(f"    name: \"{name}\"\n")
            file.write("\n")  # 每个用户记录间空一行

    print(f"数据已处理并保存到 {output_file} 文件中。")

# 调用函数
process_json_file(input_file, output_file)
