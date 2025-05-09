import gradio as gr
from source.image_converter import convert_images
from source.resize_and_crop import resizing
from source.image_namer import image_renaming
from source.tag_convert_format import tag_converting
from source.tag_modifier import tag_modifying
import shutil
import os
import datetime

INPUT_DIR = "INPUT_FILE_HERE"
OUTPUT_DIR = "OUTPUT_HERE"

#-------------------------------------------------------

# 공통 핸들러 함수
def handle_generic_feature(feature_function, description="변환", ext=None, is_queue=False, indir=INPUT_DIR, outdir=OUTPUT_DIR, input_text=None):
    if input_text:
        t1, t2, t3 = input_text

    if ext:
        result = feature_function(print, t1, ext, indir, outdir)
    else:
        if feature_function == tag_modifying:
            result = feature_function(print, t2, t3, indir, outdir)
        else:
            result = feature_function(print, indir, outdir)

    if isinstance(result, tuple):
        converted, _ = result
    else:
        converted = result

    if converted and is_queue:
        shutil.rmtree(indir, ignore_errors=True)

    return f"{converted}개 파일 {description} 완료" if converted else f"{description}할 파일 없음"

# 버튼별 동작 함수
def handle_all_image(text1,text2,text3):
    handle_generic_feature(convert_images, outdir='tmp')
    handle_generic_feature(resizing, is_queue=True, indir='tmp', outdir='tmp2')
    return handle_generic_feature(image_renaming, ext=".png", is_queue=True, indir='tmp2', input_text=[text1, text2, text3])

def handle_all_text(text1,text2,text3):
    handle_generic_feature(tag_converting, outdir='tmp')
    handle_generic_feature(tag_modifying, is_queue=True, indir='tmp', outdir='tmp2', input_text=[text1, text2, text3])
    return handle_generic_feature(image_renaming, ext=".txt", is_queue=True, indir='tmp2', input_text=[text1, text2, text3])

def handle_conversion():
    return handle_generic_feature(convert_images)

def handle_feature2():
    return handle_generic_feature(resizing)

def handle_feature3(text1,text2,text3):
    return handle_generic_feature(image_renaming, ext=".png", input_text=[text1, text2, text3])

def handle_feature4():
    return handle_generic_feature(tag_converting)

def handle_feature5(text1,text2,text3):
    return handle_generic_feature(tag_modifying, input_text=[text1, text2, text3])

def handle_feature6(text1,text2,text3):
    return handle_generic_feature(image_renaming, ext=".txt", input_text=[text1, text2, text3])

#-------------------------------------------------------

# Gradio UI 설정

with gr.Blocks() as demo:
    gr.Markdown("### Stable Diffusion Data Preprocessing Helper")

    with gr.Tab("한번에 실행") as tab1:
    
        with gr.Row():
            text1 = gr.Textbox(label="변경할 파일 이름", placeholder="ComfyUI")
            text2 = gr.Textbox(label="추가 태그(텍스트)", placeholder="밑줄->공백, 괄호 앞에 \\")
            text3 = gr.Textbox(label="삭제 태그(텍스트)", placeholder="예시 mari \\(blue archive\\)")
        with gr.Row():
            btn1 = gr.Button("(▶)이미지 일괄 변환")
        with gr.Row():
            btn2 = gr.Button("(▶)텍스트 일괄 변환")
        output = gr.Textbox(label="처리 결과")
        btn1.click(fn=handle_all_image, inputs=[text1,text2,text3], outputs=output)
        btn2.click(fn=handle_all_text, inputs=[text1,text2,text3], outputs=output)

    with gr.Tab("개별 실행") as tab2:
        with gr.Row():
            b1 = gr.Button("이미지 변환")
            b2 = gr.Button("이미지 크롭")
            b3 = gr.Button("이미지 이름 변경")

        with gr.Row():
            b4 = gr.Button("태그 형식 변환")
            b5 = gr.Button("태그 추가/삭제")
            b6 = gr.Button("태그 파일 이름 변경")

        output = gr.Textbox(label="처리 결과")
        b1.click(fn=handle_conversion, inputs=[],outputs=output)
        b2.click(fn=handle_feature2, inputs=[], outputs=output)
        b3.click(fn=handle_feature3, inputs=[text1,text2,text3], outputs=output)
        b4.click(fn=handle_feature4, inputs=[], outputs=output)
        b5.click(fn=handle_feature5, inputs=[text1,text2,text3], outputs=output)
        b6.click(fn=handle_feature6, inputs=[text1,text2,text3], outputs=output)

demo.launch()
