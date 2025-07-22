import subprocess
import argparse
import os
import shutil

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error running: {' '.join(cmd)}")
        exit(result.returncode)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="一键完成图片重命名、裁剪和视频合成")
    parser.add_argument('--pic_folder', type=str, default='in_pic', help='原始图片文件夹')
    parser.add_argument('--crop_heigh', type=int, default=50, help='裁剪像素高度')
    parser.add_argument('--crop_position', type=str, default='top', choices=['top', 'bottom'], help='裁剪位置')
    parser.add_argument('--crop_output', type=str, default='out_pic', help='裁剪后图片输出文件夹')
    parser.add_argument('--audio_folder', type=str, default='in_audio', help='音频文件夹')
    parser.add_argument('--video_output', type=str, default='out_video/myvideo.mp4', help='输出视频文件名')
    parser.add_argument('--duration', type=int, default=10, help='每张图片展示秒数')
    parser.add_argument('--clear', action='store_true', help='清空in_audio、in_pic、out_pic、out_video目录')
    args = parser.parse_args()

    if args.clear:
        clear_dir()
        exit(0)

    # 步骤1：重命名图片
    run(['python', 'rename_pics.py', '--folder', args.pic_folder])

    # 步骤2：裁剪图片
    run([
        'python', 'crop_pics.py',
        '--folder', args.pic_folder,
        '--heigh', str(args.crop_heigh),
        '--position', args.crop_position,
        '--output', args.crop_output
    ])

    # 步骤3：合成视频
    run([
        'python', 'make_video.py',
        '--audio_folder', args.audio_folder,
        '--image_folder', args.crop_output,
        '--output', args.video_output,
        '--duration', str(args.duration)
    ])

    # python book2podcast.py --pic_folder in_pic --crop_heigh 50 --crop_position bottom --crop_output out_pic --audio_folder in_audio --video_output out_video/myvideo.mp4 --duration 10
    # python book2podcast.py --clear 