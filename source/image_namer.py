import os
import shutil
import tkinter as tk
from tkinter import simpledialog

def image_renaming(log=print, ext=".png", indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    사용자로부터 텍스트를 입력받아 현재 폴더 내의 모든 지정된 확장자 파일 이름을 
    [입력텍스트]_0001.확장자 형식으로 output 폴더에 저장.
    최종 파일 이름도 함께 반환.
    """
    root = tk.Tk()
    root.withdraw()  # 메인 창 숨기기

    prefix = simpledialog.askstring("이름 지정", "새 파일 이름의 접두어를 입력하세요:", initialvalue="ComfyUI")
    if not prefix:
        log("입력이 취소되었습니다.")
        return 0, None

    ext = ext.lower().strip()
    if not ext.startswith("."):
        ext = "." + ext  # 확장자 앞에 점이 없으면 추가

    output_folder = outdir
    os.makedirs(output_folder, exist_ok=True)

    file_list = [f for f in os.listdir(indir) if f.lower().endswith(ext)]
    renamed = 0
    last_filename = None

    for i, filename in enumerate(file_list, start=1):
        filepath = os.path.join(indir, filename)
        try:
            new_name = f"{prefix}_{i:04d}{ext}"
            shutil.copy2(filepath, os.path.join(output_folder, new_name))
            log(f"[log]{filename} → {new_name}")
            renamed += 1
            last_filename = new_name
        except Exception as e:
            log(f"{filename} 이름 변경 실패: {e}")

    return renamed, last_filename
