import sqlite3
from datetime import datetime, date

class DBHelper:
	def __init__(self, dbname="movers.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname, check_same_thread = False)

	def setup(self):
		sql_file = open("script_db.sql", "r")
		script = sql_file.read().split('\n\n\n\n')
		
		for sql in script:
			print(sql)
			self.conn.execute(sql)
			self.conn.commit()


	def insert_user(self, obj):
		sql = "INSERT INTO users(chat_id, name, data_joined) VALUES (?, ?, ?);"

		self.conn.execute(sql, (obj['chat_id'], obj['name'], date.today()))
		self.conn.commit()

	def insert_car(self, obj):
		sql = "SELECT fuel_id FROM fuels WHERE fuel_type = '%s'"%obj['fuel']
		fuel_id = [x[0] for x in self.conn.execute(sql)]
		obj.pop('fuel')
		fuel_id = fuel_id[0]

		sql = "INSERT INTO cars(car_number, name, fuel_id) VALUES (?, ?, ?);"

		self.conn.execute(sql, (obj['vin'], obj['name'], fuel_id))
		self.conn.commit()

	def insert_driver(self, obj):
		sql = "SELECT car_number FROM cars WHERE car_number = '%s'"%obj['car_number']
		car_number = [x[0] for x in self.conn.execute(sql)]
		obj.pop('car_number')
		car_number = car_number[0]

		sql = "INSERT INTO drivers(name, experience, car_number) VALUES (?, ?, ?);"

		self.conn.execute(sql, (obj['name'], obj['experience'], car_number))
		self.conn.commit()

	def insert_fuel(self, obj):
		sql = "INSERT INTO fuels(fuel_type, price) VALUES (?, ?);"

		self.conn.execute(sql, (obj['fuel_type'], obj['price']))
		self.conn.commit()

	def insert_route(self, obj):
		sql = "INSERT INTO routes(name, distance, payment) VALUES (?, ?, ?);"

		self.conn.execute(sql, (obj['name'], obj['distance'], obj['payment']))
		self.conn.commit()

	def insert_transportation(self, obj):
		sql = "INSERT INTO transportations(description, route_id, start_date, end_date) VALUES (?, ?, ?, ?);"

		self.conn.execute(sql, (obj['description'], obj['route_id'], obj['start_date'], obj['end_date']))
		self.conn.commit()

	def find_transportation(self, obj):
		sql = "SELECT * FROM transportations WHERE description = '%s' AND route_id = %d"%(obj['description'],obj['route_id'])
		transportation = [x for x in self.conn.execute(sql)]

		transportation = transportation[0]
		return transportation

	def insert_transportation_driver(self, obj):
		sql = "INSERT INTO transportation_drivers(transportation_id, driver_id) VALUES (?, ?);"

		self.conn.execute(sql, (obj['transportation_id'], obj['driver_id']))
		self.conn.commit()


	def find(self, table):
		sql = "SELECT * FROM %s"%table
		return [x for x in self.conn.execute(sql)]

	def execute(self, sql):
		conn_execute = self.conn.execute(sql)
		self.conn.commit()
		return conn_execute













