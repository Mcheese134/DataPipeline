import simplejson
import flask_restful
from flask_restful import Resource, Api
from flask import Flask, jsonify, make_response, request
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin

class CommandResource(Resource):
    def get(self):
        try:
            #Provides different resources that can be used for web routes
            obj_action = request.args.get("action","")
            obj_limit = request.args.get("limit","")
            obj_type = request.args.get("type", "")
            obj_header = request.args.get("header", "")
            
            if(obj_action == "1"):
                if(int(obj_limit) <= 10):
                    return getSensor(obj_limit)
                else:
                    return make_response(jsonify('Invalid limit value'))
            elif(obj_action == "2"):
                return getDataRange(obj_limit)
            elif(obj_action == "3"):
                return getAverage(obj_type, obj_limit)
            elif(obj_action == "4"):
                return getMin(obj_type, obj_limit)
            elif(obj_action=="5"):
                return getMax(obj_type, obj_limit)
            elif(obj_action == "6"):
                return getHourlyData(obj_type, obj_limit)
            elif(obj_header == "1"):
                return getHeader(obj_limit)
            else:
                return make_response(jsonify({'error':'Not Found'}),404)
        except:
            return make_response(jsonify({'API':'Not Found'}),404)


app = Flask(__name__)
mysql = MySQL()
api = Api(app)
CORS(app)
api.add_resource(CommandResource, "/api/v1/measurement/command")


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'Insert_UserName'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Insert_Password'
app.config['MYSQL_DATABASE_DB'] = 'Insert_Database'
app.config['MYSQL_DATABASE_HOST'] = 'Insert_Host'

mysql.init_app(app)


#Queries to get average data from the past day
def getAverage(dataType, dataLimit):
    cur = mysql.connect().cursor()
    averageQuery = "SELECT AVG("+dataType+") from (select "+dataType+" from Insert_Table where Insert_Item >= now()-INTERVAL  " +dataLimit + " day AND " +dataType + ">=-Insert_LowerBound AND " + dataType+ "<= Insert_UpperBound) AS Average"
    cur.execute(averageQuery)
    avg = cur.fetchall()
    resp = jsonify(avg)
    resp.status_code = 200
    return resp

# Queries to get minimum data from the past day
def getMin(dataType, dataLimit):
    cur = mysql.connect().cursor()
    minimumQuery ="SELECT MIN("+dataType+") from (select "+dataType+" from Insert_Table where Insert_Item >= now()-INTERVAL  " +dataLimit + " day AND " +dataType + ">=-Insert_LowerBound AND " + dataType+ "<= Insert_UpperBound) AS Minimum"
    cur.execute(minimumQuery)
    minimum = cur.fetchall()
    resp = jsonify(minimum)
    resp.status_code = 200
    return resp

# Queries to get maximum data from the past day
def getMax(dataType, dataLimit):
    cur = mysql.connect().cursor()
    maxQuery ="SELECT MAX("+dataType+") from (select "+dataType+" from Insert_Table where Insert_Item >= now()-INTERVAL  " +dataLimit + " day AND " +dataType + ">=-Insert_LowerBound AND " + dataType+ "<= Insert_UpperBound) AS Maximum"
    cur.execute(maxQuery)
    maximum = cur.fetchall()
    resp = jsonify(maximum)
    resp.status_code = 200
    return resp

# Queries to get hourly data for up to a certain limit
def getHourlyData(dataType, dataLimit):
    cur = mysql.connect().cursor()
    hourlyQuery = "Select " + dataType +" FROM Insert_Table Group by Insert_TimeStamp DIV 3600 desc limit " + dataLimit; 
    cur.execute(hourlyQuery)
    hourly = cur.fetchall()
    resp = jsonify(hourly)
    resp.status_code = 200
    return resp

#Queries to get latest data from a sensor up to a certain limit in the database
def getSensor(dataLimit):

    sensorQuery = "select Insert_Items from Insert_Table order by Insert_TimeStamp desc limit " + dataLimit

    #This mySQL query is to retrieve all the attributes for one row 
    allAtt = 'select * from Insert_Table limit 1'
      
    cur = mysql.connect().cursor()
    
    #Used to retrieve header values and number of attributes
    cur.execute(allAtt)
    totalColNum = len(cur.description)
    allCol = cur.description
    
    #Retrieve the sensor data from the sensorQuery 
    cur.execute(sensorQuery)
    rows = cur.fetchall()
    
    #formats the data into a list that can be later used for JSON format
    num = list(sum(rows, ()))
    count = 0
    variable = []

    #
    arrayMap = {}

    #Map the number of attributes in a dictionary via its name and column position in the table
    #Create a 2d array with the number of arrays equal to the attribute amount
    for i in range(totalColNum):
        temp = []     
        arrayMap[allCol[i][0]] = i
        variable.append(temp)

    #Allocate the correct data to its position in the array which is later jsonified
    for i, element in enumerate(num):

        index= arrayMap.get(cur.description[count][0])
        num[i] = str(num[i])
        variable[index].append(num[i])
        count+=1

        if(count == len(cur.description)):
            count = 0

    resp = jsonify( Data1 = variable[2], Data2 = variable[4], Data3 = variable[6], Data4 = variable[9])
    resp.status_code = 200
    return resp

#Returns the headers of a table
def getHeader(dataLimit):
        cur = mysql.connect().cursor()
        temp = "select Insert_Items from Insert_Table order by Insert_TimeStamp desc limit 1"
        cur.execute(temp)
        row = cur.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp

#same as get sensor except specifies what range of dates to take data from
def getDataRange():
    cur = mysql.connect().cursor()
    temp = "SELECT Insert_Items FROM Insert_Table WHERE Insert_Items BETWEEN 'Date1' AND 'Date2' limit 10"

    if('limit' in temp):
        limit = int(temp.split('limit')[1])

    cur.execute(temp)
    rows = cur.fetchall()

    num = list(sum(rows,()))
    variable = []
    count = 0


    for i in range(len(cur.description)):
        temp = []
        variable.append(temp)

    for i, element in enumerate(num):
        num[i] = cur.description[count][0] + ': ' + str(num[i])
        variable[count].append(num[i])
        count+=1

        if(count == len(cur.description)):
            count = 0

    resp = jsonify( Data1 = variable[0], Data2 = variable[1], Data3 = variable[2], Data4 = variable[3] )
    
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
