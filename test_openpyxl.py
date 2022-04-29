from openpyxl import Workbook
wb = Workbook()
sheet1 = wb.active
sheet1.title = "helloWorld"
print(sheet1.title)
wb.save("helloworld.xlsx")

wb = ()
