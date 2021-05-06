#python 解析pdf文件
import os,sys
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams,LTFigure
#图片解析模块
from PIL import Image
import pytesseract #（1）首先下载tesseract-ocr。下载地址为百度网盘：https://pan.baidu.com/s/1OL0g1MBzeijD23JN0UGC0Q
# 配置https://blog.csdn.net/weixin_41644725/article/details/95344924?utm_medium=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-1.control&dist_request_id=1329188.9106.16178490919224771&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromMachineLearnPai2~default-1.control
import fitz

# #文件路径
# path="D:/jyj/2022王道操作系统.pdf"
# # path="D:/jyj/test.pdf"
# file_flag=os.path.exists(path)
# #print(file_flag)
#
# # with open(path,'r',encoding='utf-8') as f:
# #     t=f.read()
# #     print(t)
#
# fb=open(path,'rb')#二进制打开文件
#
# #用文件对象来创建一个pdf文档分析器
# praser=PDFParser(fb)
# #pdf文档的对象
# doc=PDFDocument()
# #链接文档对象
# praser.set_document(doc)
# doc.set_parser(praser)
# #初始化文档，当前文档没有密码设置为空字符
# doc.initialize("")
#
# # 检测文档是否提供txt转换，不提供就忽略
# if not doc.is_extractable:
#     raise PDFTextExtractionNotAllowed
# else:
#     # 创建PDf 资源管理器 来管理共享资源
#     rsrcmgr = PDFResourceManager()
#     # 创建一个PDF设备对象
#     laparams = LAParams()
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#     # 创建一个PDF解释器对象
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#     # 循环遍历列表，每次处理一个page的内容
#     for page in doc.get_pages():  # doc.get_pages() 获取page列表
#         interpreter.process_page(page)
#         # 接受该页面的LTPage对象
#         layout = device.get_result()
#         # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
#         for x in layout:
#             # print(x)
#             if (isinstance(x, LTTextBoxHorizontal)):#文字对象
#                 # 需要写出编码格式
#                 # 解决\u8457\u5f55\u683c\u5f0f\uff1a\u67cf\u6167乱码
#                 results = x.get_text().encode('raw_unicode_escape').decode('unicode_escape')
#                 print(results)
#             # if (isinstance(x,LTFigure)):#图片对象
#             #     print('ok')

# imgs_save_path = "D:/jyj/python/image/"
imgs_save_path="D:/jyj/发票/"
pdf_path="D:/jyj/发票/北京地铁03.pdf"

def PDF_to_imgs(path, save_path):
    # 打开PDF文件，生成一个对象
    doc = fitz.open(path)
    # 将PDF文件的每一页都转化为图片
    for pg in range(doc.pageCount):
        page = doc[pg]
        print(page)
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4倍的图像。
        zoom_x = 2
        zoom_y = 2
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(save_path + '%s.png' % pg)
        print(save_path+'%s.png'%pg)
# #图片文字解析
# for files,_,files_names in os.walk(imgs_save_path):
#     for file_name in files_names:
#         print(files+file_name)
#         image=Image.open(files+file_name)
#         txt=pytesseract.image_to_string(image,lang='chi_sim')
#         print(txt)
PDF_to_imgs(pdf_path,imgs_save_path)

