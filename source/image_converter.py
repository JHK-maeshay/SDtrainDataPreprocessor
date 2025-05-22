import os
import shutil
from PIL import Image
from .counter_decorator import counter_deco

@counter_deco
def __jpg_convert__(log, filepath, filename, outdir):
    img = Image.open(filepath).convert("RGB")
    base = os.path.splitext(filename)[0]
    new_name = base + ".png"
    img.save(os.path.join(outdir, new_name), "PNG")
    log(f"[log]변환 완료: {filename} → {new_name}")

@counter_deco
def __png_convert__(log, filepath, filename, outdir):
    # PNG는 변환 없이 복사
    shutil.copy2(filepath, os.path.join(outdir, filename))
    log(f"[log]이동 완료: {filename}")
        
def convert_images(log, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    os.makedirs(outdir, exist_ok=True)
    convert_exts = [".jpg", ".jpeg", ".webp"]
    file_list = os.listdir(indir)
    for filename in file_list:
        ext = os.path.splitext(filename)[1].lower()
        filepath = os.path.join(indir, filename)
        try:
            if ext in convert_exts:
                __jpg_convert__(log, filepath, filename, outdir)
            elif ext == ".png":
                __png_convert__(log, filepath, filename, outdir)
        except Exception as e:
            log(f"처리 실패: {filename} ({e})")
    return __jpg_convert__.counter['count']+__png_convert__.counter['count']

