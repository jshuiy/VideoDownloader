import re

# 文件路径
input_file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\before_url.txt'
output_file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\after_url.txt'

# 读取文件内容
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取YouTube视频链接
    video_links = re.findall(r'https://www\.youtube\.com/watch\?v=[\w-]+', content)

    # 去重处理
    unique_video_links = list(set(video_links))

    # 输出提取到的链接并写入到 after_url.txt 文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        if unique_video_links:
            file.write("提取到的唯一视频链接：\n")
            for link in unique_video_links:
                file.write(link + '\n')
            print(f"已将 {len(unique_video_links)} 个去重后的视频链接写入到 {output_file_path} 文件中。")
        else:
            file.write("未找到任何视频链接。\n")
            print("未找到任何视频链接。")
except FileNotFoundError:
    print(f"文件未找到: {input_file_path}")
