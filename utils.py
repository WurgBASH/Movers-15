import xlrd, xlwt
import json

def read_table(file, data_set):
	data = xlrd.open_workbook(file_contents=file.read())
	sheet = data.sheet_by_index(0)
	vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
	vals.pop(0)
	objects_array = []

	if data_set == 1:	#cars
		for row in vals:
			row[2] = str(row[2])
			if row[2][-1] == "0":
				row[2] = row[2][:-2]
			obj = {"name": row[0], "vin": row[1], "fuel": row[2]}
			objects_array.append(obj)
		export_data = json.dumps(objects_array, ensure_ascii=False)

	elif data_set == 2:	#drivers
		for row in vals: 
			obj = {"name": row[0], "experience": int(row[1]), "car_number": row[2]}
			objects_array.append(obj)
		export_data = json.dumps(objects_array, ensure_ascii=False)

	elif data_set == 3:	#routes
		for row in vals: 
			obj = {"name": row[0], "distance": row[1], "payment": row[2]}
			objects_array.append(obj)
		export_data = json.dumps(objects_array, ensure_ascii=False)

	return objects_array


def write_table(file, data_set):
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Page')

	if file == 1:	#driver payment
		ws.write(0, 0, "ФIO")	
		ws.write(1, 0, data_set[0])

		ws.write(0, 1, "Нараховано")
		ws.write(1, 1, data_set[1])

		ws.write(0, 2, "Премія")
		ws.write(1, 2, data_set[2])

		ws.write(0, 3, "Період")
		ws.write(1, 3, data_set[3])

		wb.save('driver_payment.xls')

		return('driver_payment.xls')

	elif file == 2:	#transport price

		ws.write(0, 0, "Маршрут")	
		ws.write(1, 0, data_set[0])

		ws.write(0, 1, "Водій")
		ws.write(1, 1, data_set[1])

		ws.write(0, 2, "Дата відправлення")
		ws.write(1, 2, data_set[2])

		ws.write(0, 3, "Дата прибуття")
		ws.write(1, 3, data_set[3])

		wb.save('transport_price.xls')

		return('transport_price.xls')

data_s = ("фамілєя імя отчества", "насчітано", "премушечька", "периода длинна")
write_table(2, data_s)