#!/bin/bash

# Get the directory where the script is located
BASE_DIR=$(dirname "$0")

# Change to the script's directory
cd "$BASE_DIR"

VENV_DIR="venv"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for python3
if ! command_exists python3; then
    echo "错误：找不到 python3。"
    echo "请先安装 Python 3 (https://www.python.org/downloads/macos/)。"
    read -p "按 Enter 键退出。"
    exit 1
fi

echo "欢迎使用 Book2Podcast！"
echo "正在准备启动环境，请稍候..."
echo "----------------------------------------"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "错误：创建虚拟环境失败。"
        read -p "按 Enter 键退出。"
        exit 1
    fi
    echo "虚拟环境创建成功。"
    echo ""
    echo "正在安装所需依赖库，这可能需要几分钟时间..."
    source "$VENV_DIR/bin/activate"
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误：安装依赖库失败。"
        echo "请检查您的网络连接或 'requirements.txt' 文件是否正确。"
        read -p "按 Enter 键退出。"
        exit 1
    fi
    echo "依赖库安装完成。"
else
    echo "检测到已存在的虚拟环境，将直接启动。"
    source "$VENV_DIR/bin/activate"
fi

echo "----------------------------------------"
echo "环境准备就绪！"
echo ""
echo "正在启动 Web UI 服务..."
echo "服务启动后，将自动在浏览器中打开操作页面。"
echo ""
echo "您可以随时通过关闭此终端窗口来停止服务。"
echo "----------------------------------------"

# Start the web server and automatically open the browser
# We need to find an available port and then open the browser.
# Gradio by default uses 7860. Let's start the python script
# and then open the browser.
(sleep 10 && open http://127.0.0.1:7860) &

python3 web.py

echo "服务已关闭。感谢使用！"
