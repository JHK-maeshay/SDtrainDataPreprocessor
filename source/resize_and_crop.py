from PIL import Image
import os
from .counter_decorator import counter_deco

def get_best_target(size, target_sizes):
        w, h = size
        aspect = w / h
        return min(target_sizes, key=lambda s: abs((s[0] / s[1]) - aspect))

@counter_deco
def __resize__(log, filename, filepath, target_sizes, outdir):
    img = Image.open(filepath)
    orig_w, orig_h = img.size
    target_w, target_h = get_best_target(img.size, target_sizes)

    # Resize maintaining aspect ratio
    orig_aspect = orig_w / orig_h
    target_aspect = target_w / target_h

    if orig_aspect > target_aspect:
        new_h = target_h
        new_w = int(orig_w * (target_h / orig_h))
    else:
        new_w = target_w
        new_h = int(orig_h * (target_w / orig_w))

    img = img.resize((new_w, new_h), Image.LANCZOS)

    # 중앙 크롭
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    new_name = os.path.splitext(filename)[0] + f"_resized.png"
    img.save(os.path.join(outdir, new_name))
    log(f"[log]{filename} → {new_name} (비율: {target_w}x{target_h})")
     

def resizing(log=print, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    현재 폴더 내의 모든 PNG 이미지를 1344x768, 1024x1024, 768x1344 중 가장 근사한 비율로 변환하여 저장.
    기존 비율 유지하며 한쪽을 맞추고, 남는 부분은 중앙에서 크롭.
    """
    target_sizes = [(1344, 768), (1024, 1024), (768, 1344)]
    file_list = [f for f in os.listdir(indir) if f.lower().endswith(".png")]
    os.makedirs(outdir, exist_ok=True)

    for filename in file_list:
        filepath = os.path.join(indir, filename)
        try:
            __resize__(log, filename, filepath, target_sizes, outdir)
        except Exception as e:
            log(f"{filename} 변환 실패: {e}")

    rt = __resize__.counter['count']
    __resize__.reset_count()

    return rt