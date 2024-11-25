import requests
import json
import time
import urllib3

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 请求头
headers = {
    "xweb_xhr": "1",
    "x-token": "x-token",  # 替换为实际抓包中的动态 Token
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275",
    "token": "db3f69df-92ba-4061-84d1-f248166c005b1732456422",  # 替换为实际抓包中的 Token
    "content-type": "application/json; charset=UTF-8",
    "accept": "*/*",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://servicewechat.com/wx9ddd73d26fdbacba/290/page-frame.html",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9"
}

# 保存所有爬取的数据
all_posts = []

# 爬取首页帖子列表
def fetch_posts():
    url = "https://www.dolacc.cn/api/Wxpostv2/getPostsv2"
    toId = 0
    scId = 59  # 根据抓包实际数据
    pageSize = 10
    lastIndex = 1942507  # 替换为实际抓包的 lastindex 值

    while True:
        params = {
            "toId": toId,
            "scId": scId,
            "pageSize": pageSize,
            "lastindex": lastIndex,
            "keyword": ""
        }

        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            data = response.json()
            # print("接口返回数据：", json.dumps(data, ensure_ascii=False, indent=2))

            # 提取 posts 列表
            posts = data.get("data", {}).get("posts", [])
            if not isinstance(posts, list):
                print("错误：posts 不是列表，数据提取异常")
                break

            if not posts:
                print("所有帖子已抓取完成")
                break

            # 将抓取到的 posts 添加到 all_posts 列表
            all_posts.extend(posts)
            print(f"抓取到 {len(posts)} 条帖子，累计 {len(all_posts)} 条帖子")

            # 如果累计抓取的数据大于等于 1000 条，结束爬取
            if len(all_posts) >= 1000:
                print("累计抓取超过 1000 条帖子，停止爬取")
                break

            # 更新 lastIndex 为当前批次的最后一条帖子的 index
            try:
                lastIndex = posts[-1].get("id", lastIndex)
            except Exception as e:
                print(f"未知错误: {e}")
                break

            # 每次抓取后保存数据到文件
            with open("posts.json", "w", encoding="utf-8") as f:
                json.dump(all_posts, f, ensure_ascii=False, indent=4)
            print("当前数据已保存到 posts.json")

            time.sleep(1)  # 防止请求过快被封

        else:
            print(f"请求失败，状态码: {response.status_code}")
            break

# 主程序
if __name__ == "__main__":
    print("开始抓取首页帖子列表...")
    fetch_posts()
    print("抓取完成，最终数据已保存到 posts.json")
