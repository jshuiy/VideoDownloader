import requests

# 要爬取的网页 URL
url = 'https://www.youtube.com/watch?v=VIDxQ7JOItg'  # 替换为你要爬取的网页链接

# 文件路径
output_file = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\before_url.txt'

# 发送 GET 请求，获取网页内容
try:
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，抛出异常
    html_content = response.text  # 获取网页的 HTML 内容

    # 将 HTML 内容写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
        print(f"成功将网页内容写入到 {output_file} 文件中。")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
