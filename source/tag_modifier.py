import os
import tkinter as tk
from tkinter import simpledialog

class TagInputDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("태그 추가/삭제")
        
        tk.Label(master, text="추가할 태그: *언더바->공백, 괄호 앞에 \\").grid(row=0, sticky="w")
        self.add_entry = tk.Entry(master, width=40)
        self.add_entry.insert(0, "")
        self.add_entry.grid(row=1, padx=10, pady=(0,10))

        tk.Label(master, text="삭제할 태그: *예시 mari \\(blue archive\\)").grid(row=2, sticky="w")
        self.remove_entry = tk.Entry(master, width=40)
        self.remove_entry.insert(0, "")
        self.remove_entry.grid(row=3, padx=10, pady=(0,10))

        return self.add_entry  # 첫 번째 포커스 위치

    def apply(self):
        self.result = {
            "add": self.add_entry.get(),
            "remove": self.remove_entry.get()
        }

def clean_tag_input(raw):
    """쉼표로 구분된 문자열에서 공백, 빈 값 제거 및 중복 제거."""
    return [tag.strip() for tag in raw.split(",") if tag.strip()]

def tag_modifying(log=print, indir='INPUT_FILE_HERE', outdir='OUTPUT_HERE'):
    """
    사용자로부터 추가/삭제할 태그를 입력받고,
    각 txt파일에서 해당 태그들을 처리하여 output 폴더에 저장.
    """
    root = tk.Tk()
    root.withdraw()

    # 사용자 입력 받기
    dialog = TagInputDialog(root)
    if dialog.result:
        add_input = dialog.result["add"]
        remove_input = dialog.result["remove"]

        add_tags = clean_tag_input(add_input)
        remove_tags = clean_tag_input(remove_input)
        print("[debug]추가 태그:", add_tags)
        print("[debug]삭제 태그:", remove_tags)
    root.destroy()
    
    # 합쳐서 중복 제거된 삭제용 집합 만들기
    remove_set = set(add_tags + remove_tags)

    file_list = [f for f in os.listdir(indir) if f.lower().endswith(".txt")]
    os.makedirs(outdir, exist_ok=True)
    modified = 0

    for filename in file_list:
        filepath = os.path.join(indir, filename)
        try:
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
            modified += 1
        except Exception as e:
            log(f"{filename} 처리 실패: {e}")

    return modified
