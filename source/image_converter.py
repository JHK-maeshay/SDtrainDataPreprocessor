import os
import shutil
from PIL import Image

def convert_images(log, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    output_folder = outdir
    os.makedirs(output_folder, exist_ok=True)

    convert_exts = [".jpg", ".jpeg", ".webp"]
    file_list = os.listdir(indir)
    converted = 0

    for filename in file_list:
        ext = os.path.splitext(filename)[1].lower()
        filepath = os.path.join(indir, filename)
        try:
            if ext in convert_exts:
                img = Image.open(filepath).convert("RGB")
                base = os.path.splitext(filename)[0]
                new_name = base + ".png"
                img.save(os.path.join(output_folder, new_name), "PNG")
                log(f"[log]변환 완료: {filename} → {new_name}")
                converted += 1
            elif ext == ".png":
                # PNG는 변환 없이 복사
                shutil.copy2(filepath, os.path.join(output_folder, filename))
                log(f"[log]이동 완료: {filename}")
                converted += 1
        except Exception as e:
            log(f"처리 실패: {filename} ({e})")

    return converted

