"""教科書PDF(data/)から文楽クイズ用の図を切り出して assets/img/ に保存する（ビルド時のみ使用）。
依存: pip install pymupdf pillow
実行: python tools/extract_figures.py  （リポジトリルートから）
座標は「回転後ページ」を 100dpi でレンダリングした画像 (約818x1161) 上のピクセル。
"""
import io
import os
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
DPI = 200
BASE = 100  # 座標の基準dpi

# (出力名, PDF, 回転角, (x0, y0, x1, y1) @100dpi 回転後座標)
FIGURES = [
    ("tayu_tools.png", "CCI20261101.pdf", 0, (545, 245, 790, 435)),
    ("stage.png", "CCI20261101_0001.pdf", 180, (15, 110, 790, 540)),
    ("sanshin.png", "CCI20261101_0005.pdf", 180, (445, 245, 720, 585)),
    ("hayashi.png", "CCI20261101_0005.pdf", 180, (60, 710, 770, 900)),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, pdf, rot, box in FIGURES:
        doc = pymupdf.open(os.path.join(ROOT, "data", pdf))
        page = doc[0]
        page.set_rotation((page.rotation + rot) % 360)
        pix = page.get_pixmap(dpi=DPI)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
        k = DPI / BASE
        crop = img.crop(tuple(int(v * k) for v in box))
        if crop.width > 1000:  # 配信サイズ削減
            crop = crop.resize((1000, round(crop.height * 1000 / crop.width)), Image.LANCZOS)
        path = os.path.join(OUT, name)
        crop.save(path, optimize=True)
        print(name, crop.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
