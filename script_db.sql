
CREATE TABLE routes
(
	route_id  INTEGER NULL,
	name  VARCHAR(20) NOT NULL,
	distance  INTEGER NOT NULL,
	payment  INTEGER NOT NULL,
	 PRIMARY KEY (route_id)
)
;



CREATE UNIQUE INDEX XPKroutes ON routes
(
	route_id
)
;



CREATE TABLE transportations
(
	transportation_id  INTEGER NULL,
	description  VARCHAR(20) NULL,
	route_id  INTEGER NULL,
	start_date DATE NULL,
	end_date  DATE NULL,
	PRIMARY KEY (transportation_id) 
	FOREIGN KEY (route_id) REFERENCES routes(route_id)
)
;



CREATE UNIQUE INDEX XPKtransportations ON transportations
(
	transportation_id
)
;



CREATE INDEX XIF1transportations ON transportations
(
	route_id
)
;



CREATE TABLE fuels
(
	fuel_id  INTEGER NULL,
	fuel_type  VARCHAR(20) NULL,
	price  FLOAT NOT NULL,
	PRIMARY KEY (fuel_id)
)
;



CREATE UNIQUE INDEX XPKfuels ON fuels
(
	fuel_id
)
;



CREATE TABLE cars
(
	car_number  VARCHAR(20) NULL,
	name  VARCHAR(20) NULL,
	fuel_id  INTEGER NULL,
	PRIMARY KEY (car_number)
	FOREIGN KEY (fuel_id) REFERENCES fuels(fuel_id)
)
;



CREATE UNIQUE INDEX XPKcars ON cars
(
	car_number
)
;



CREATE INDEX XIF1cars ON cars
(
	fuel_id
)
;



CREATE TABLE drivers
(
	driver_id  INTEGER NULL,
	name  VARCHAR(20) NULL,
	experience  INTEGER NULL,
	car_number  VARCHAR(20) NULL,
	PRIMARY KEY (driver_id)
	FOREIGN KEY (car_number) REFERENCES cars(car_number)
)
;



CREATE UNIQUE INDEX XPKdrivers ON drivers
(
	driver_id
)
;



CREATE INDEX XIF1drivers ON drivers
(
	car_number
)
;



CREATE TABLE transportation_drivers
(
	transportation_id  INTEGER NOT NULL,
	driver_id  INTEGER NOT NULL,
	PRIMARY KEY (transportation_id, driver_id)
	FOREIGN KEY (transportation_id) REFERENCES transportations(transportation_id),
	FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
)
;



CREATE UNIQUE INDEX XPKtransportation_drivers ON transportation_drivers
(
	transportation_id,
	driver_id
)
;



CREATE INDEX XIF2transportation_drivers ON transportation_drivers
(
	transportation_id
)
;



CREATE INDEX XIF3transportation_drivers ON transportation_drivers
(
	driver_id
)
;



CREATE TABLE users
(
	chat_id  INTEGER NULL,
	name  VARCHAR(20) NULL,
	data_joined  DATE NULL,
	 PRIMARY KEY (chat_id)
)
;



CREATE UNIQUE INDEX XPKusers ON users
(
	chat_id
)
;


