import re
import yt_dlp
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/save": {"origins": "*"}, r"/extract": {"origins": "*"}, r"/download": {"origins": "*"}})

# 定义文件保存路径
before_file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\before_url.txt'
after_file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\after_url.txt'
download_path = r"C:\Users\qilon\OneDrive\桌面\demo"

# 返回 HTML 页面
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 处理保存请求
@app.route('/save', methods=['POST'])
def save_text():
    data = request.get_json()
    text = data.get('text', '')

    if text:
        try:
            with open(before_file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            return jsonify({"message": "内容已成功保存到 before_url.txt 文件中。"}), 200
        except Exception as e:
            return jsonify({"message": f"保存内容时出错: {e}"}), 500
    else:
        return jsonify({"message": "文本内容为空，无法保存。"}), 400

# 处理提取请求
@app.route('/extract', methods=['POST'])
def extract_links():
    try:
        with open(before_file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip().splitlines()
        
        print("读取的内容:", content)  # 调试信息

        video_links = []
        for line in content:
            if 'href="/watch?v=' in line:
                start_index = line.find('/watch?v=')
                full_link = f'https://www.youtube.com{line[start_index:line.find("\"", start_index)]}'
                video_links.append(full_link)

        print("拼接后的链接:", video_links)  # 调试信息

        unique_video_links = list(set(video_links))

        with open(after_file_path, 'w', encoding='utf-8') as file:
            if unique_video_links:
                file.write("提取到的唯一视频链接：\n")
                for link in unique_video_links:
                    file.write(link + '\n')
                return jsonify({"message": f"已将 {len(unique_video_links)} 个去重后的视频链接写入到 {after_file_path} 文件中。"}), 200
            else:
                file.write("未找到任何视频链接。\n")
                return jsonify({"message": "未找到任何视频链接。"}), 200
    except FileNotFoundError:
        return jsonify({"message": f"文件未找到: {before_file_path}"}), 404

# 处理下载请求
@app.route('/download', methods=['POST'])
def download_videos():
    file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\after_url.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        video_links = re.findall(r'https://www\.youtube\.com/watch\?v=[\w-]+', content)

        download_path = "C:\\Users\\qilon\\OneDrive\\桌面\\demo"

        if video_links:
            for url in video_links:
                try:
                    ydl_opts = {
                        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                        'format': 'bestvideo+bestaudio/best',
                        'merge_output_format': 'mp4',
                        'postprocessors': [{
                            'key': 'FFmpegMerger'
                        }],
                        'progress_hooks': [lambda d: print(f"Downloading {d['filename']}...") if d['status'] == 'downloading' else None]
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    print(f"Downloaded: {url}")
                except Exception as e:
                    print(f"Error downloading {url}: {e}")

            return jsonify({"message": "下载完成！"}), 200
        else:
            return jsonify({"message": "未找到任何视频链接。"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
