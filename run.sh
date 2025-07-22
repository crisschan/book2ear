#!/bin/bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
# 安装依赖
pip install -r requirements.txt

# 启动 web.py（后台运行）
python3 web.py &

# 等待 Gradio 启动（可根据实际情况调整等待时间）
while ! nc -z 127.0.0.1 7860; do
  sleep 1
done

# 自动打开浏览器
open http://127.0.0.1:7860