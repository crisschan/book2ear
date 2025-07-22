import gradio as gr
import os
import shutil
import subprocess

def save_uploaded_files(uploaded_files, target_dir):
    # 清空目标目录
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    # 保存所有上传的文件
    for file_path in uploaded_files:
        filename = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(target_dir, filename))

def save_uploaded_audio(uploaded_file, target_dir):
    # 清空目标目录
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    # 只保存一个音频文件
    filename = os.path.basename(uploaded_file)
    shutil.copy(uploaded_file, os.path.join(target_dir, filename))

def clear_dir():
    for d in ['out_video','in_audio', 'in_pic', 'out_pic']:
        folder = d
        if not os.path.exists(folder):
            print(f"{folder} does not exist.")
            continue
        # 如果是out_video且目录为空，则停止循环
        if folder == 'out_video' and len(os.listdir(folder)) == 0:
            print(f"{folder} is empty, stop clearing other folders.")
            break
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
        print(f"Cleared {folder}")

def run_book2podcast(pic_files, audio_file, crop_heigh, crop_position, crop_output, video_output, duration):
    # 检查是否上传了图片和音频
    clear_dir()
    if not pic_files or len(pic_files) == 0:
        yield "请上传至少一张图片文件。", None
        return
    if not audio_file:
        yield "请上传一个音频文件。", None
        return

    pic_folder = "in_pic"
    audio_folder = "in_audio"

    # 保存上传的图片和音频
    save_uploaded_files(pic_files, pic_folder)
    save_uploaded_audio(audio_file, audio_folder)

    # 确保输出文件夹存在
    os.makedirs(crop_output, exist_ok=True)
    os.makedirs(os.path.dirname(video_output), exist_ok=True)

    # 调用主脚本
    cmd = [
        'python', 'book2podcast.py',
        '--pic_folder', pic_folder,
        '--crop_heigh', str(crop_heigh),
        '--crop_position', crop_position,
        '--crop_output', crop_output,
        '--audio_folder', audio_folder,
        '--video_output', video_output,
        '--duration', str(duration)
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = ""
    for line in proc.stdout:
        output += line
        yield output, None
    proc.wait()
    if proc.returncode == 0 and os.path.exists(video_output):
        yield output + f"\n处理完成！输出视频: {video_output}", video_output
    else:
        yield output + "\n出错了！", None

def download_video_file(video_path):
    if video_path and os.path.exists(video_path):
        return video_path
    else:
        raise gr.Error("视频文件还未生成，请先点击开始处理并等待完成！")

with gr.Blocks() as demo:
    gr.Markdown("# BookBookBook")
    with gr.Row():
        with gr.Column(scale=1):
            pic_files = gr.Files(label="上传图片文件夹（多选）", file_count="multiple", type="filepath", scale=1)
        with gr.Column(scale=1):
            audio_file = gr.File(label="上传音频文件（单个）", type="filepath", scale=1)
            output = gr.Textbox(label="输出信息", lines=10, scale=1)
    with gr.Row():
        run_btn = gr.Button("开始处理")
        # download_btn = gr.Button("下载视频")
        download_file = gr.File(label="生成视频下载", interactive=True)
    with gr.Row():
        crop_heigh = gr.Number(label="裁剪高度", value=50)
        crop_position = gr.Radio(["top", "bottom"], label="裁剪位置", value="bottom")
        crop_output = gr.Textbox(label="裁剪后图片输出文件夹", value="out_pic")
    with gr.Row():
        video_output = gr.Textbox(label="输出视频文件名", value="out_video/myvideo.mp4")
        duration = gr.Number(label="每张图片展示秒数", value=10)

    # 用于存储生成的视频文件路径
    video_file_state = gr.State(value=None)

    def update_video_file_state(output_text, video_path):
        return gr.update(value=output_text), gr.update(value=None), video_path

    run_btn.click(
        run_book2podcast,
        inputs=[pic_files, audio_file, crop_heigh, crop_position, crop_output, video_output, duration],
        outputs=[output, download_file],
    )
    # download_btn.click(
    #     download_video_file,
    #     inputs=[video_output],
    #     outputs=download_file
    # )
    # 清空目录时也清空下载控件
    # def clear_dirs_and_reset():
    #     for out, _ in clear_dirs():
    #         yield out, None
    # 你可以加一个清空按钮，如果需要

if __name__ == "__main__":
    demo.launch()
