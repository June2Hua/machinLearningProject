import numpy as np
import xlrd

FILENAME = "data.xlsx" #文件的名字
file = xlrd.open_workbook(FILENAME)

table = file.sheets()[0]

print(table.nrows)

print(file.ncols)

print(file.row_values(0))

print(file.col_values(0))

print(file.cell(0,0).value)

print(np.ones([10,1]))


