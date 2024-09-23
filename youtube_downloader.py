import re
import yt_dlp

# 文件路径
file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\after_url.txt'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正则表达式提取YouTube视频链接
video_links = re.findall(r'https://www\.youtube\.com/watch\?v=[\w-]+', content)

# 下载保存路径
download_path = "C:\\Users\\qilon\\OneDrive\\桌面\\demo"

# 下载视频
if video_links:
    for url in video_links:
        try:
            ydl_opts = {
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # 指定输出文件路径和格式
                'format': 'bestvideo+bestaudio/best',  # 下载最好的视频和音频格式
                'merge_output_format': 'mp4',  # 合并后的输出格式
                'postprocessors': [{
                    'key': 'FFmpegMerger'  # 合并视频和音频
                }],
                'progress_hooks': [lambda d: print(f"Downloading {d['filename']}...") if d['status'] == 'downloading' else None]  # 显示下载进度
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print(f"Downloaded: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
else:
    print("未找到任何视频链接。")
