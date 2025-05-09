# -*- coding: utf-8 -*-

import os
import shutil
import datetime
import customtkinter as ctk
from tkinter import messagebox
from source.image_converter import convert_images
from source.resize_and_crop import resizing
from source.image_namer import image_renaming
from source.tag_convert_format import tag_converting
from source.tag_modifier import tag_modifying
#--------------------------------------------------------------
INPUT_DIR = "INPUT_FILE_HERE"
OUTPUT_DIR = "OUTPUT_HERE"
BACKUP_DIR = "backup"
#--------------------------------------------------------------
# 기본 설정
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("768x480")
app.title("이미지 변환 도구")

# 로그
def log(msg):
    print(msg)  # 필요시 터미널 로그만 출력

#--------------------------------------------------------------

# 경로설정
def set_dir(path):
    p = path
    os.makedirs(p, exist_ok=True)

def dir_input():
    set_dir(INPUT_DIR)

def dir_output():
    set_dir(OUTPUT_DIR)

# 백업
def backup(ext=["jpg"], indir=INPUT_DIR, backdir=BACKUP_DIR):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M")
    backdir = backdir+"_"+timestamp
    os.makedirs(backdir, exist_ok=True)

    file_list = os.listdir(indir)
    backed_up = 0

    for filename in file_list:
        __ext__ = os.path.splitext(filename)[1].lower()
        filepath = os.path.join(indir, filename)
        try:
            if __ext__ in ext:
                shutil.copy2(filepath, os.path.join(backdir, filename))
                backed_up += 1
        except Exception as e:
            log(f"[log]백업 실패: {filename} ({e})")

    log(f"[log]{backed_up}개 파일 백업 생성됨")

#--------------------------------------------------------------

def handle_generic_feature(
        feature_function, 
        description="변환", 
        ext=None, 
        is_queue=False, 
        indir=INPUT_DIR, 
        outdir=OUTPUT_DIR, 
        skip=False
    ):
    progress_bar.set(0.2)
    app.update_idletasks()

    # 함수 실행 결과 받기 (단일 값 또는 튜플)
    if ext:
        result = feature_function(log, ext, indir, outdir)
    else:
        result = feature_function(log, indir, outdir)

    # 결과 파싱
    if isinstance(result, tuple):
        converted, final_filename = result
    else:
        converted = result
        final_filename = None  # 기본값

    progress_bar.set(0.6)
    if converted and is_queue:
        if os.path.exists(indir) and os.path.isdir(indir):
            shutil.rmtree(indir)

    progress_bar.set(1.0)
    if not skip:
        if converted == 0:
            messagebox.showinfo("결과", f"{description}할 파일이 없습니다.")
        else:
            messagebox.showinfo("결과", f"output 폴더에 {converted}개 파일이 {description}되었습니다.")


# 변환 핸들러
def handle_all_image():
    handle_generic_feature(convert_images, description="변환", outdir='tmp', skip=True)
    handle_generic_feature(resizing, description="변환", is_queue=True, indir='tmp', outdir='tmp2', skip=True)
    handle_generic_feature(image_renaming, description="변환", ext=".png", is_queue=True, indir='tmp2')

def handle_all_text():
    handle_generic_feature(tag_converting, description="변환", outdir='tmp', skip=True)
    handle_generic_feature(tag_modifying, description="변환", is_queue=True, indir='tmp', outdir='tmp2', skip=True)
    handle_generic_feature(image_renaming, description="변환", ext=".txt", is_queue=True, indir='tmp2')

def handle_conversion():
    handle_generic_feature(convert_images, description="변환")

def handle_feature2():
    handle_generic_feature(resizing, description="변환")

def handle_feature3():
    handle_generic_feature(image_renaming, description="변환", ext=".png")

def handle_feature4():
    handle_generic_feature(tag_converting, description="변환")

def handle_feature5():
    handle_generic_feature(tag_modifying, description="변환")

def handle_feature6():
    handle_generic_feature(image_renaming, description="변환", ext=".txt")

#--------------------------------------------------------------

# 버튼 프레임
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=40)

# 버튼
buttons = []
top_button1 = ctk.CTkButton(button_frame\
, text="이미지 일괄 변환", fg_color="green", command=handle_all_image)
top_button1.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

top_button2 = ctk.CTkButton(button_frame\
, text="텍스트 일괄 변환", fg_color="green", command=handle_all_text)
top_button2.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
for i in range(6):
    if i == 0:
        btn = ctk.CTkButton(button_frame\
, text="이미지 변환", command=handle_conversion)
    elif i == 1:
        btn = ctk.CTkButton(button_frame\
, text="이미지 크롭", command=handle_feature2)
    elif i == 2:
        btn = ctk.CTkButton(button_frame\
, text="이미지 이름 변경", command=handle_feature3)
    elif i == 3:
        btn = ctk.CTkButton(button_frame\
, text="태그 형식 변환", command=handle_feature4)
    elif i == 4:
        btn = ctk.CTkButton(button_frame\
, text="태그 추가/삭제", command=handle_feature5)
    elif i == 5:
        btn = ctk.CTkButton(button_frame\
, text="태그 파일 이름 변경", command=handle_feature6)
        
    btn.grid(row=i // 3 + 2, column=i % 3, padx=10, pady=10, ipadx=10, ipady=10)
    buttons.append(btn)

# 진행 바
progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.set(0)
progress_bar.pack(pady=20)

app.mainloop()
