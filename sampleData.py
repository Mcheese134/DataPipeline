import random 
import time
import datetime
import mysql.connector as mariadb
import hashlib

#This file is coincides with the API and it shows how to send data to a database which the API utilizes

mariadb_connection = mariadb.connect(user = 'insert_Username', password = 'insert_Password', database = 'insert_Database', host = 'insert_Host')
cursor = mariadb_connection.cursor()

#Used to initialize a checksum 
m = hashlib.md5()


#Initialize sample data
pressure = '0.00'
pressureUnit = 'ATM'

force = '0.00'
forceUnit = 'lb'

weight = '0.00'
weightUnit = 'kg'

#updates the new value of the checksum
m.update(pressure+pressure+force+forceUnit+weight+weightUnit)

while(1):

	pressure = str(round(random.uniform(70.00, 70.99), 2))
	force = str(round(random.uniform(0, 1000), 2) )
	weight = str(round(random.uniform(0, 100),2 ) )
	
	#used if you wanted to get current timestamp
	currentDT = datetime.datetime.now()

	#update the checksum to a new value and store it
	m.update(pressure + pressureUnit + force +forceUnit + weight + weightUnit)
	checksum = m.hexdigest()

	#insert the data to the database, commit, and loop for 5 seconds
	try:
		cursor.execute("INSERT INTO Insert_Table(InsertItem, InsertItem, InsertItem, ... ) VALUES (%s, %s, %s, %s, %s, %s)", (pressure, pressureUnit, force, forceUnit, weight, weightUnit ))
	except mariadb.Error as error:
		print("Error: {}".format(error))

	mariadb_connection.commit()
	
	time.sleep(5)
