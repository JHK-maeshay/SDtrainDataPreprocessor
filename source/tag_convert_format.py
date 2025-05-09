import os

def tag_converting(log=print, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    현재 폴더의 모든 .txt 파일에서:
    - '_'를 ' '로,
    - '('를 '\('로,
    - ')'를 '\)'로 변환하여
    동일한 이름으로 output 폴더에 저장.
    """
    file_list = [f for f in os.listdir(indir) if f.lower().endswith(".txt")]
    output_folder = outdir
    os.makedirs(output_folder, exist_ok=True)
    converted = 0

    for filename in file_list:
        filepath = os.path.join(indir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            content = content.replace("_", " ")
            content = content.replace("(", r"\(")
            content = content.replace(")", r"\)")

            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            log(f"[log]{filename} 변환 완료 → output/{filename}")
            converted += 1
        except Exception as e:
            log(f"{filename} 처리 중 오류 발생: {e}")

    return converted
