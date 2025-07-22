import os
import re

def rename_pic(folder="in_pic"): 
    for filename in os.listdir(folder):
        match = re.search(r'(\d+)', filename)
        if match:
            number = match.group(1)
            ext = os.path.splitext(filename)[1]
            new_name = f"{number}{ext}"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            if old_path != new_path and not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
            elif old_path != new_path:
                print(f"Skipped (target exists): {filename} -> {new_name}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='批量重命名图片文件，只保留数字和扩展名')
    parser.add_argument('--folder', type=str, default='in_pic', help='图片文件夹')
    args = parser.parse_args()
    rename_pic(folder=args.folder)
    # python rename_pics.py --folder in_pic