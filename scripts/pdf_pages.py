"""把课本扫描 PDF 渲染成便于阅读的 PNG（可旋转、可把双页跨页拆成左右两页）。

用法：
    python pdf_pages.py 扫描.pdf 输出目录 [--rotate 90] [--split] [--dpi 110] [--pages 1,3-4]

--rotate  逆时针旋转角度。手机扫描的跨页常是顺时针躺倒的，用 90 扶正
--split   扶正后按宽度对半切成左右两页（跨页扫描时用）
先用低 dpi 看一眼方向，再按需要重新渲染。
"""
import argparse
from pathlib import Path

import fitz
from PIL import Image


def page_list(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(total))
    result = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        result += list(range(int(a) - 1, int(b or a)))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--rotate", type=int, default=0)
    ap.add_argument("--split", action="store_true")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--pages")
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    for i in page_list(args.pages, len(doc)):
        pix = doc[i].get_pixmap(dpi=args.dpi)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if args.rotate:
            img = img.rotate(args.rotate, expand=True)
        parts = [img.crop((0, 0, img.width // 2, img.height)), img.crop((img.width // 2, 0, img.width, img.height))] \
            if args.split else [img]
        for k, part in enumerate(parts):
            name = f"p{i + 1:02d}" + ("ab"[k] if args.split else "") + ".png"
            part.save(out / name)
            print(out / name)


if __name__ == "__main__":
    main()
