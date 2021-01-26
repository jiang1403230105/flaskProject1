#解析excel表
import openpyxl

filename='D:\jyj\国家统计局数据\快速查询.xlsx'

wb = openpyxl.load_workbook(filename)

print(wb.sheetnames)