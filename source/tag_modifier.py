import os
from .counter_decorator import counter_deco

@counter_deco
def __modify__(log, filename, filepath, add_tags, remove_set, outdir):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    words = [w.strip() for w in content.split(",") if w.strip()]
    # 기존 단어 중 삭제 대상 제거
    remaining_words = [w for w in words if w not in remove_set]
    # 앞에 추가 태그 삽입
    final_words = add_tags + remaining_words

    with open(os.path.join(outdir, filename), "w", encoding="utf-8") as f:
        f.write(", ".join(final_words))

    log(f"[log]{filename} 처리 완료 → output/{filename}")

def clean_tag_input(raw):
    """쉼표로 구분된 문자열에서 공백, 빈 값 제거 및 중복 제거."""
    return [tag.strip() for tag in raw.split(",") if tag.strip()]

def tag_modifying(log=print, add_input=None, remove_input=None, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    사용자로부터 추가/삭제할 태그를 입력받고,
    각 txt파일에서 해당 태그들을 처리하여 output 폴더에 저장.
    """
    add_tags = clean_tag_input(add_input)
    remove_tags = clean_tag_input(remove_input)
    print("[debug]추가 태그:", add_tags)
    print("[debug]삭제 태그:", remove_tags)
    
    # 합쳐서 중복 제거된 삭제용 집합 만들기
    remove_set = set(add_tags + remove_tags)

    file_list = [f for f in os.listdir(indir) if f.lower().endswith(".txt")]
    os.makedirs(outdir, exist_ok=True)

    for filename in file_list:
        filepath = os.path.join(indir, filename)
        try:
            __modify__(log, filename, filepath, add_tags, remove_set, outdir)
        except Exception as e:
            log(f"{filename} 처리 실패: {e}")

    rt = __modify__.counter['count']
    __modify__.reset_count()
    return rt
