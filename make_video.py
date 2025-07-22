import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def make_video(audio_folder='in_audio', image_folder='out_pic', output='out_video/output.mp4', duration_per_image=8):
    # 确保输出目录存在
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 取第一个音频文件
    audio_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(('.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg'))]
    if not audio_files:
        print('No audio file found!')
        return
    audio_path = os.path.join(audio_folder, sorted(audio_files)[0])
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    print(f'Audio duration: {audio_duration}')

    # 按文件名排序图片
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))],
                        key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else x)
    if not image_files:
        print('No image file found!')
        return

    clips = []
    total_time = 0
    for i, img in enumerate(image_files):
        if i < len(image_files) - 1:
            clip = ImageClip(os.path.join(image_folder, img)).set_duration(duration_per_image)
            total_time += duration_per_image
        else:
            # 最后一张图片展示到音频结束
            last_duration = max(audio_duration - total_time, 0.1)
            clip = ImageClip(os.path.join(image_folder, img)).set_duration(last_duration)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    # 为了避免后续fps的变化导数音频文件长度和视频文件长度一致的情况下后尾有重复的问题，
    # 这里audio_duration 进行了int的方法进行处理，这并不能保证全部的音视频都适用
    video = video.set_audio(audio_clip).set_duration(int(audio_duration))
    video.write_videofile(output, fps=25, audio_codec='aac')
    print(f'Video saved as {output}')
    # print(f'Video saved as {output}')
    print(f'Video duration: {video.duration}')

    # 清空图片目录
    for f in os.listdir(image_folder):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                os.remove(os.path.join(image_folder, f))
            except Exception as e:
                print(f"Failed to remove {f}: {e}")
    print(f'Cleared all images in {image_folder}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='将音频和图片合成为视频')
    parser.add_argument('--audio_folder', type=str, default='in_audio', help='音频文件夹')
    parser.add_argument('--image_folder', type=str, default='out_pic', help='图片文件夹')
    parser.add_argument('--output', type=str, default='out_video/output.mp4', help='输出视频文件名')
    parser.add_argument('--duration', type=int, default=8, help='每张图片展示秒数')
    args = parser.parse_args()
    make_video(audio_folder=args.audio_folder, image_folder=args.image_folder, output=args.output, duration_per_image=args.duration) 