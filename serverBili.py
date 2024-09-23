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
        # 读取输入文件的内容
        with open(before_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        print("读取的内容:", content)  # 调试信息

        # 用于存储去重后的 YouTube 和 Bilibili 链接
        youtube_links = set()
        bilibili_links = set()

        # 提取完整的 YouTube 视频链接
        full_youtube_links = re.findall(r'https://www\.youtube\.com/watch\?v=[\w-]+', content)
        if full_youtube_links:
            # 如果找到完整的 YouTube 链接，直接使用这些链接
            youtube_links.update(full_youtube_links)
        else:
            # 如果没有找到完整链接，提取 href="/watch?v=..." 格式的链接
            youtube_matches = re.findall(r'href="/watch\?v=[\w-]+"', content)
            for match in youtube_matches:
                full_link = f'https://www.youtube.com{match[6:-1]}'  # 去除 href=" 并添加 https://www.youtube.com
                youtube_links.add(full_link)

        # 提取完整的 Bilibili 视频链接
        full_bilibili_links = re.findall(r'https://www\.bilibili\.com/video/[\w-]+(?:\?t=\d+(?:\.\d+)?|/?)', content)
        if full_bilibili_links:
            # 如果找到完整的 Bilibili 链接，直接使用这些链接
            bilibili_links.update(full_bilibili_links)
        else:
            # 如果没有找到完整链接，提取 href="//www.bilibili.com/video/..." 格式的链接
            bilibili_matches = re.findall(r'href="//www\.bilibili\.com/video/[\w-]+(?:\?t=\d+(?:\.\d+)?|/?)"', content)
            for match in bilibili_matches:
                full_link = f'https:{match[6:-1]}'  # 去除 href=" 并添加 https:
                bilibili_links.add(full_link)

        print("去重后的 YouTube 链接:", youtube_links)  # 调试信息
        print("去重后的 Bilibili 链接:", bilibili_links)  # 调试信息

        # 将去重后的链接写入到文件
        with open(after_file_path, 'w', encoding='utf-8') as file:
            # 写入去重后的 YouTube 视频链接
            if youtube_links:
                file.write("提取到的唯一 YouTube 视频链接：\n")
                for link in youtube_links:
                    file.write(link + '\n')

            # 写入去重后的 Bilibili 视频链接
            if bilibili_links:
                file.write("\n提取到的唯一 Bilibili 视频链接：\n")
                for link in bilibili_links:
                    file.write(link + '\n')

        # 返回处理结果
        total_links = len(youtube_links) + len(bilibili_links)
        return jsonify({"message": f"已将 {total_links} 个去重后的视频链接写入到 {after_file_path} 文件中。"}), 200

    except FileNotFoundError:
        return jsonify({"message": f"文件未找到: {before_file_path}"}), 404
    except Exception as e:
        return jsonify({"message": f"处理时出错: {e}"}), 500


# 处理下载请求
@app.route('/download', methods=['POST'])
def download_videos():
    file_path = r'C:\Users\qilon\OneDrive\桌面\YoutubeDL\after_url.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        youtube_links = re.findall(r'https://www\.youtube\.com/watch\?v=[\w-]+', content)
        bilibili_links = re.findall(r'https://www\.bilibili\.com/video/[BVbv][\w-]+', content)

        if youtube_links or bilibili_links:
            for url in youtube_links + bilibili_links:
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
