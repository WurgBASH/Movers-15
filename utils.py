import xlrd, xlsxwriter
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

	if file == 1:	#driver payment
		workbook = xlsxwriter.Workbook('driver_payment.xlsx')
		worksheet = workbook.add_worksheet()
		header = workbook.add_format()
		header.set_font_size(25)

		titles = workbook.add_format()
		titles.set_font_size(15)
		titles.set_align('center')
		titles.set_bold()

		data_cells = workbook.add_format()
		data_cells.set_align('vjustify')


		cell_format = workbook.add_format()

		worksheet.set_column('A1:A', 80)
		worksheet.set_column('A2:A2', 20)
		worksheet.set_column('B2:B2', 20)
		worksheet.set_column('C2:C2', 20)
		worksheet.set_column('D2:D2', 20)


		bold = workbook.add_format({'bold': True})

		worksheet.write('A1', 'Відомість про заробітну плату водіїв', header)

		worksheet.write('A3', 'ФIO', titles)
		worksheet.write('A4', data_set[0], data_cells)
		worksheet.write('B3', 'Нараховано', titles)
		worksheet.write('B4', data_set[1], data_cells)
		worksheet.write('C3', 'Премія', titles)
		worksheet.write('C4', data_set[2], data_cells)
		worksheet.write('D3', 'Період', titles)
		worksheet.write('D4', data_set[3], data_cells)
		workbook.close()

		return('driver_payment.xlsx')

		
	elif file == 2:	#transport price
		workbook = xlsxwriter.Workbook('transport_price.xlsx')
		worksheet = workbook.add_worksheet()
		header = workbook.add_format()
		header.set_font_size(25)

		titles = workbook.add_format()
		titles.set_font_size(15)
		titles.set_align('center')
		titles.set_align('vjustify')
		titles.set_bold()

		data_cells = workbook.add_format()
		data_cells.set_align('vjustify')


		cell_format = workbook.add_format()

		worksheet.set_column('A1:A', 80)
		worksheet.set_column('A2:A2', 20)
		worksheet.set_column('B2:B2', 20)
		worksheet.set_column('C2:C2', 20)
		worksheet.set_column('D2:D2', 20)


		bold = workbook.add_format({'bold': True})

		worksheet.write('A1', 'Відомість про заробітну плату водіїв', header)

		worksheet.write('A3', 'Маршрут', titles)
		worksheet.write('A4', data_set[0], data_cells)
		worksheet.write('B3', 'Водій', titles)
		worksheet.write('B4', data_set[1], data_cells)
		worksheet.write('C3', 'Дата відправлення', titles)
		worksheet.write('C4', data_set[2], data_cells)
		worksheet.write('D3', 'Дата прибуття', titles)
		worksheet.write('D4', data_set[3], data_cells)
		workbook.close()

		return('transport_price.xlsx')