#python 解析pdf文件
import os,sys
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams

#文件路径
path="D:/jyj/guokao/公共基础知识5000题+答案解析/决战公共基础知识5000题1(题本).pdf"
file_flag=os.path.exists(path)
print(file_flag)
with open(path,'r',encoding='utf-8') as f:
    t=f.read()
    print(t)

# fb=open(path,'rb')#二进制打开文件
#
# #用文件对象来创建一个pdf文档分析器
# praser=PDFParser(fb)
#
# doc=PDFDocument()
#
# praser.set_document(doc)
# doc.set_parser(praser)
# doc.initialize()
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
#             if (isinstance(x, LTTextBoxHorizontal)):
#                 # 需要写出编码格式
#                 # 解决\u8457\u5f55\u683c\u5f0f\uff1a\u67cf\u6167乱码
#                 results = x.get_text().encode('raw_unicode_escape').decode('unicode_escape')
#                 print(results)
