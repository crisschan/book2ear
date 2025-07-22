import os
from PIL import Image

def crop_image(input_path, output_path, heigh, position='bottom'):
    with Image.open(input_path) as img:
        width, height = img.size
        if heigh >= height:
            print(f"Skip {input_path}: heigh >= image height")
            return
        if position == 'top':
            box = (0, heigh, width, height)
        elif position == 'bottom':
            box = (0, 0, width, height - heigh)
        else:
            print(f"Invalid position: {position}")
            return
        cropped = img.crop(box)
        cropped.save(output_path)
        print(f"Cropped {input_path} -> {output_path}")

def batch_crop(folder='in_pic', heigh=100, position='bottom', output_folder=None):
    if output_folder is None:
        output_folder = folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(folder, filename)
            output_path = os.path.join(output_folder, filename)
            crop_image(input_path, output_path, heigh, position)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='批量裁剪图片顶部或底部')
    parser.add_argument('--folder', type=str, default='in_pic', help='图片文件夹')
    parser.add_argument('--heigh', type=int, required=True, help='裁剪像素高度')
    parser.add_argument('--position', type=str, choices=['top', 'bottom'], default='bottom', help='裁剪位置')
    parser.add_argument('--output', type=str, default=None, help='输出文件夹（默认为覆盖原文件）')
    args = parser.parse_args()
    batch_crop(folder=args.folder, heigh=args.heigh, position=args.position, output_folder=args.output) 

    # 裁剪底部 100 像素（覆盖原文件）
    # python crop_pics.py --heigh 100 --position bottom

    # # 裁剪顶部 50 像素，结果保存到 out_pic 文件夹
    # python crop_pics.py --heigh 50 --position top --output out_pic