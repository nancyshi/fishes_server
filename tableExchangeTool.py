import xlrd
import json

fileName = "boatIntensifyConfig"
workbook = xlrd.open_workbook(fileName + ".xlsx")
sheet = workbook.sheet_by_index(0)
titleNum = sheet.ncols
titles = []

for oneCol in range(0,titleNum):
    title = sheet.cell(0,oneCol).value
    titles.append(title)

result = []
for row in range(1,sheet.nrows):
    dic = {}
    for col in range(0, sheet.ncols):
        oneTitle = titles[col]
        value = sheet.cell(row,col).value
        if oneTitle == "id" or oneTitle == "boatLevel" or oneTitle == "level" or oneTitle == "neededDollor" or oneTitle == "Parameter1" or oneTitle == "Parameter2":
            value = int(value)
        dic[oneTitle] = value
    result.append(dic)

with open(fileName + ".json","w") as f:
    json.dump(result,f,indent = 4)
