import xlrd
import json

def read_table(file, data_set):

	data = xlrd.open_workbook(file, formatting_info=True)
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
			obj = {"name": row[0], "expirience": int(row[1]), "car_number": row[2]}
			objects_array.append(obj)
		export_data = json.dumps(objects_array, ensure_ascii=False)

	elif data_set == 3:	#routes
		for row in vals: 
			obj = {"name": row[0], "distance": row[1], "payment": row[2]}
			objects_array.append(obj)
		export_data = json.dumps(objects_array, ensure_ascii=False)

	return(export_data)