"""
    基于FastAPI的后端纠错API接口服务
    先加载文本纠错模型预热再启动后端接口服务
"""

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sutil import cut_sent, replace_char, get_paragraphs_text
import uvicorn
import paddlehub as hub
import cv2
from paddlenlp import Taskflow
import time

print("模型加载预热！")
# OCR文本识别
ocr = hub.Module(name="chinese_ocr_db_crnn_server")
ocr_results = ocr.recognize_text (images=[cv2.imread('./resource/imagetest.jpg')])

print("PaddleOCR图片识别结果：")
print(ocr_results)
# 处理识别结果
toCorrectText = []
for i in range(len(ocr_results[0]['data'])):
    toCorrectText.append(str(ocr_results[0]['data'][i]['text']))

# PaddleNLP 文本纠错
text_correction = Taskflow("text_correction")
# 纠错结果处理
print("PaddleNLP文本纠错结果：")
for idx, item in enumerate(toCorrectText):    
    res = text_correction(item)
    if (len(res[0]['errors'])) > 0:
        for i, error in enumerate(res[0]['errors']):
            if i == 0:
                item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), res[0]['errors'][i]['position'])
            else:
                # 如果句子中有多处错字，那么每替换前面一个字，后面的错字索引往后移动3位：即括号+字=3位
                p = res[0]['errors'][i]['position'] + i * 3
                item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), p)
        print(item)
    else:
        print(item)

# 创建一个 FastAPI「实例」，名字为app
app = FastAPI()

# 设置允许跨域请求，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体数据类型：text
class Document(BaseModel):
    text: str

# 定义路径操作装饰器：POST方法 + API接口路径

# 文本纠错接口
@app.post("/v1/textCorrect/", status_code=200)
# 定义路径操作函数，当接口被访问将调用该函数
async def TextErrorCorrection(document: Document):
    try:
        # 获取要进行纠错的文本内容
        text = document.text
        # 精细分句处理以更好处理长文本
        data = cut_sent(text)
        
        # 进行文本纠错和标记
        correctionResult = ''
        for idx, item in enumerate(data):
            if item != "":
                res = text_correction(item)
                length = len(res[0]['errors'])
                if length > 0:
                    for i, error in enumerate(res[0]['errors']):
                        if i == 0:
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), res[0]['errors'][i]['position'])
                        else:
                            # 如果句子中有多处错字，那么每替换前面一个字，后面的错字索引往后移动3位：即括号+字=3位
                            p = res[0]['errors'][i]['position'] + i * 3
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), p)
                if item is not '':
                    correctionResult += item;
                    correctionResult += '\n';

        # 接口结果返回
        results = {"message": "success", "originalText": document.text, "correctionResults": correctionResult}
        return results
    # 异常处理
    except Exception as e:
        print("异常信息：", e)
        raise HTTPException(status_code=500, detail=str("请求失败，服务器端发生异常！异常信息提示：" + str(e)))

# 文档纠错接口
@app.post("/v1/docCorrect/", status_code=200)
# 定义路径操作函数，当接口被访问将调用该函数
async def DocumentErrorCorrection(file: UploadFile):
    # 读取上传的文件
    docBytes = file.file.read()
    docName = file.filename
    # 判断上传文件类型
    docType = docName.split(".")[-1]
    if docType != "doc" and docType != "docx":
        raise HTTPException(status_code=406, detail=str("请求失败，上传文档格式不正确！请上传word文档！"))
    try:
        # 将上传文件保存到本地，添加时间标记避免重复
        now_time = int(time.mktime(time.localtime(time.time())))
        docPath = "./resource/" + str(now_time) + "_" + docName
        fout = open(docPath, 'wb')
        fout.write(docBytes)
        fout.close()

        # 读取要进行文本纠错的word文档内容
        docText = get_paragraphs_text(docPath)
        # 对word文档内容进行分句处理避免句子过长
        docText = cut_sent(docText)

        # 进行文本纠错和标记
        correctionResult = ""
        for idx, item in enumerate(docText):
            if item is not '':
                res = text_correction(item)
                length = len(res[0]['errors'])
                if length > 0:
                    for i, error in enumerate(res[0]['errors']):
                        if i == 0:
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), res[0]['errors'][i]['position'])
                        else:
                            # 如果句子中有多处错字，那么每替换前面一个字，后面的错字索引往后移动3位：即括号+字=3位
                            p = res[0]['errors'][i]['position'] + i * 3
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), p)
                if item is not '':
                    correctionResult += item;
                    correctionResult += '\n';

        # 接口结果返回
        results = {"message": "success", "docText": str(docText), "correctionResults": correctionResult}
        return results
    # 异常处理
    except Exception as e:
        print("异常信息：", e)
        raise HTTPException(status_code=500, detail=str("请求失败，服务器端发生异常！异常信息提示：" + str(e)))

# 图片纠错接口
@app.post("/v1/imageCorrect/", status_code=200)
# 定义路径操作函数，当接口被访问将调用该函数
async def ImageErrorCorrection(file: UploadFile):
    # 读取上传的文件
    imgBytes = file.file.read()
    imgName = file.filename
    # 判断上传文件类型
    imgType = imgName.split(".")[-1]
    if imgType != "png" and imgType != "jpg" and imgType != "jpeg" :
        raise HTTPException(status_code=406, detail=str("请求失败，上传图片格式不正确！请上传jpg或png图片！"))
    try:
        now_time = int(time.mktime(time.localtime(time.time())))
        # 拼接生成随机文件名，注意名称不能包含中文否则后面读取出错
        imgPath = "./resource/" + str(now_time) + "_image." + imgType
        print(imgPath)
        fout = open(imgPath, 'wb')
        fout.write(imgBytes)
        fout.close()
        print("文件上传成功！")

        # OCR文本识别
        ocr_image_results = ocr.recognize_text(images=[cv2.imread(imgPath)])

        # 处理图片识别文本结果
        toCorrectText = []
        for i in range(len(ocr_image_results[0]['data'])):
            toCorrectText.append(str(ocr_image_results[0]['data'][i]['text']))

        # 进行文本纠错和标记
        correctionResult = ""
        for idx, item in enumerate(toCorrectText):
            if item != "":
                res = text_correction(item)
                length = len(res[0]['errors'])
                if length > 0:
                    for i, error in enumerate(res[0]['errors']):
                        if i == 0:
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), res[0]['errors'][i]['position'])
                        else:
                            # 如果句子中有多处错字，那么每替换前面一个字，后面的错字索引往后移动3位：即括号+字=3位
                            p = res[0]['errors'][i]['position'] + i * 3
                            item = replace_char(item, (list(res[0]['errors'][i]['correction'].keys())[0] + '（' + list(res[0]['errors'][i]['correction'].values())[0] + '）'), p)
                if item is not '':
                    correctionResult += item;
                    correctionResult += '\n';

        # 接口结果返回
        results = {"message": "success", "orcResult": str(ocr_image_results[0]), "correctionResults": correctionResult}
        return results
    # 异常处理
    except Exception as e:
        print("异常信息：", e)
        raise HTTPException(status_code=500, detail=str("请求失败，服务器端发生异常！异常信息提示：" + str(e)))

# 启动创建的实例app，设置启动ip和端口号
uvicorn.run(app, host="127.0.0.1", port=8000)
