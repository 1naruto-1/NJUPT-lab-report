"""整理用户拍的手绘电路图、手绘波形、示波器照片：摆正、裁剪、可选提亮纸面。

用法：
    python prep_image.py 原图 输出图 [--rotate 90] [--crop 0.1,0.05,0.9,0.7] [--clean]

--rotate  逆时针旋转角度（EXIF 方向会先自动处理）
--crop    按比例裁剪：左,上,右,下（0~1）
--clean   让纸面更白、笔迹更清楚（只做整体亮度/对比度调整，不改动笔迹内容）
"""
import argparse

from PIL import Image, ImageOps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--rotate", type=int, default=0)
    ap.add_argument("--crop")
    ap.add_argument("--clean", action="store_true")
    args = ap.parse_args()
    img = ImageOps.exif_transpose(Image.open(args.src)).convert("RGB")
    if args.rotate:
        img = img.rotate(args.rotate, expand=True)
    if args.crop:
        l, t, r, b = (float(v) for v in args.crop.split(","))
        img = img.crop((int(l * img.width), int(t * img.height), int(r * img.width), int(b * img.height)))
    if args.clean:
        gray = ImageOps.autocontrast(ImageOps.grayscale(img), cutoff=(2, 1))
        img = gray.point(lambda v: 255 if v > 200 else v).convert("RGB")
    img.save(args.dst, quality=92)
    print(args.dst, img.size)


if __name__ == "__main__":
    main()
