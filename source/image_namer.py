import os
import shutil
from .counter_decorator import counter_deco

@counter_deco
def __rename__(log, i, filename, filepath, prefix, ext, outdir):
    new_name = f"{prefix}_{i:04d}{ext}"
    shutil.copy2(filepath, os.path.join(outdir, new_name))
    log(f"[log]{filename} → {new_name}")
    return new_name

def image_renaming(log=print, prefix='comfyUI', ext=".png", indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    지정한 접두어(prefix)를 사용해 현재 폴더 내의 모든 지정된 확장자 파일 이름을 
    [prefix]_0001.확장자 형식으로 output 폴더에 저장.
    """
    if not prefix:
        log("입력이 비어있습니다.")
        return 0, None

    ext = ext.lower().strip()
    if not ext.startswith("."):
        ext = "." + ext

    os.makedirs(outdir, exist_ok=True)

    file_list = [f for f in os.listdir(indir) if f.lower().endswith(ext)]
    last_filename = None

    for i, filename in enumerate(file_list, start=1):
        filepath = os.path.join(indir, filename)
        try:
            last_filename = __rename__(log, i, filename, filepath, prefix, ext, outdir)
        except Exception as e:
            log(f"{filename} 이름 변경 실패: {e}")

    rt = __rename__.counter['count']
    __rename__.reset_count()

    return rt, last_filename