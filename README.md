# Book2Ear

## 项目简介

Book2Ear 是一个将书籍图片和音频合成为视频的工具，可以帮助用户将电子书或实体书的图片内容与朗读音频结合，生成可在各种设备上播放的视频文件。这个工具特别适合制作有声读物、学习材料或将书籍内容转换为可听形式。

## 功能特点

- **图片处理**：自动重命名和裁剪图片，支持顶部或底部裁剪
- **视频合成**：将图片和音频合成为视频，自动调整图片展示时长
- **批处理**：支持批量处理多张图片
- **Web界面**：提供友好的Web界面，无需命令行操作
- **命令行支持**：同时支持命令行操作，方便脚本集成

## 安装说明

### 环境要求

- Python 3.12+
- 依赖库：gradio, moviepy, Pillow

### 安装步骤

1. 克隆仓库或下载源码

```bash
git clone https://github.com/yourusername/book2ear.git
cd book2ear
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### Web界面使用

1. 启动Web服务

```bash
python web.py
```

2. 在浏览器中打开显示的URL（通常是 http://127.0.0.1:7860）
3. 上传图片文件（可多选）
4. 上传一个音频文件
5. 设置裁剪参数和视频参数
6. 点击"开始处理"按钮
7. 处理完成后，可以下载生成的视频

### 命令行使用

#### 一键处理

```bash
python book2podcast.py --pic_folder in_pic --crop_heigh 50 --crop_position bottom --crop_output out_pic --audio_folder in_audio --video_output out_video/myvideo.mp4 --duration 10
```

#### 清空工作目录

```bash
python book2podcast.py --clear
```

#### 单独使用各模块

**重命名图片**
```bash
python rename_pics.py --folder in_pic
```

**裁剪图片**
```bash
python crop_pics.py --heigh 50 --position top --output out_pic
```

**制作视频**
```bash
python make_video.py --audio_folder in_audio --image_folder out_pic --output out_video/output.mp4 --duration 8
```

## 目录结构

- `in_pic/`: 存放原始图片的目录
- `out_pic/`: 存放处理后图片的目录
- `in_audio/`: 存放音频文件的目录
- `out_video/`: 存放生成视频的目录
- `book2podcast.py`: 主程序，整合所有功能
- `rename_pics.py`: 图片重命名工具
- `crop_pics.py`: 图片裁剪工具
- `make_video.py`: 视频合成工具
- `web.py`: Web界面程序

## 参数说明

### book2podcast.py 参数

- `--pic_folder`: 原始图片文件夹，默认为 'in_pic'
- `--crop_heigh`: 裁剪像素高度，默认为 50
- `--crop_position`: 裁剪位置，可选 'top' 或 'bottom'，默认为 'top'
- `--crop_output`: 裁剪后图片输出文件夹，默认为 'out_pic'
- `--audio_folder`: 音频文件夹，默认为 'in_audio'
- `--video_output`: 输出视频文件名，默认为 'out_video/myvideo.mp4'
- `--duration`: 每张图片展示秒数，默认为 10
- `--clear`: 清空工作目录

## 注意事项

1. 图片文件名中应包含数字，以便正确排序
2. 音频文件将按字母顺序选择第一个文件
3. 处理完成后，图片文件会被自动清理
4. Web界面处理时会自动清空所有工作目录

## 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。
