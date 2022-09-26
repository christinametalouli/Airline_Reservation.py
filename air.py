from pymongo import MongoClient, cursor
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import pymongo
import json
from bson import ObjectId
from bson.json_util import dumps
import time
import random

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSAirline']

# Choose collections
users = db['Users']
reservations = db['Reservations']
flights = db['Flights']




#initiate Flask app
app = Flask(__name__)
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


@app.route('/')

# create simple user
@app.route('/createSimpleUser', methods=['POST'])
def create_simple_user():
    global user_category
    
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "email" in data or not "password" in data or not "passport" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # if user not in database already / checking email, username and passport
    if not(users.find_one({"email":data["email"]})) and not(users.find_one({"username":data["username"]})) and not(users.find_one({"passport":data["passport"]})) :
	# update user_category for simple user
        passw = data["password"]
        if len(passw) > 7 and has_numbers(passw):
            user_category = {"user_category":'simple user'}
            data.update(user_category)
            users.insert_one(data) # add user
            return Response("User "+data['username']+" was added.\n", mimetype='application/json', status=200) 
        else:
            return Response("wrong", mimetype='application/json', status=400)
    else: # if user already in database 
        return Response("A user with this information already exists\n", mimetype='application/json', status=400) 


# login
@app.route('/login', methods=['POST'])
def login():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    # if email or usename or password is not given
    if (not "email" in data and not "username" in data) or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    
    if "email" in data :
        user1 = users.find_one({"email" : data['email'] })
    elif "username" in data :
        user1= users.find_one({"username" : data['username']})
    else:
        return Response("Wrong information.", status=400 , mimetype='application/json')
    if user1['password'] == data['password'] :  
      
       global user_category
       global currentUser
       
       currentUser = str(user1['name'])
       
       user_category = str(user1['user_category'])
       
       return Response("Logged in.",status=200 , mimetype='application/json') 
    else :
            return Response("Wrong password.", status=400 , mimetype='application/json')
     



# Search flight
@app.route('/search', methods=['POST',' GET'])
def search():
    # check user 
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")

    # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    if not "departure_destination"  in data or not "arrival_destination" in data or not "departure_date" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    searchedFlight = flights.find_one({"departure_destination" :data["departure_destination"], "arrival_destination" :data["arrival_destination"],"departure_date" :data["departure_date"] })
    
    ticketsCount = int(searchedFlight["tickets"])
    if ticketsCount >=1 :
        return Response(dumps(searchedFlight), status=200, mimetype='application/json') #emfanizei ola ta arxeia 
             
    else:
        return Response('No free seets left',status=500,mimetype='application/json')
      




# resevation
@app.route('/reservation', methods=['POST',' GET'])
def reservation():
     # check user 
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    if not "flight_id"  in data or not "name" in data or not "passport" in data or not "card" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    new_card = str(data["card"])
    if len(new_card) == 16:    
        new_card = {'card':data["card"]}
        new_reservation = {'flight_id':data["flight_id"], 'name':data["name"], 'passport':data["passport"], 'card':data["card"],'reservation_id':data["reservation_id"]}
        reservations.insert_one(new_reservation)

        sFlight = flights.find_one({"flight_id" :data["flight_id"]})
        tCount = int(sFlight["tickets"])
        tCount = tCount - 1
        flights.update_one({"flight_id":data['flight_id']},{"$set":{"tickets":tCount}})

        return Response(dumps(new_reservation),status=500,mimetype="application/json")
    else:
        return Response("Card number must be 16 digits",status=500,mimetype="application/json")




# show reservation
@app.route('/showReservation',methods=['GET'])
def showReservation():
   # check user 
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")

    # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    if not "reservation_id"  in data:
       return Response("Information incomplete",status=500,mimetype="application/json")
      
    searchedReservation = reservations.find_one({"reservation_id" :data["reservation_id"]})

    return Response(dumps(searchedReservation), status=200, mimetype='application/json')

        



# Delete reservation
@app.route('/deleteReservation', methods=['POST',' GET'])
def deleteReservation():
    # check user 
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")

    # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    if not "reservation_id"  in data :
        return Response("Information incomplete",status=500,mimetype="application/json")
    

    reserv = reservations.find_one({"reservation_id" :data["reservation_id"]})

    card_no = str(reserv["card"])

    reservations.delete_one({"reservation_id": data["reservation_id"]})

    
    return Response(f"Reservation deleted. Your money is back in the card: {card_no}",status=200 , mimetype='application/json')


# Search destination
@app.route('/searchDestination',methods=['GET'])
def searchDestination():
   # check user 
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")

    # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')

    if not "arrival_destination"  in data:
       return Response("Information incomplete",status=500,mimetype="application/json")
      

    searchedF = flights.find_one({"arrival_destination" :data["arrival_destination"]})

    flight_no = str(searchedF["flight_id"])
   
    res = reservations.find_one({"flight_id":searchedF["flight_id"]})
     
    res_no = str(res["flight_id"])

    if flight_no == (res_no):

        return Response(dumps(res), status=200, mimetype='application/json')
    else:
         return Response("There is no reservation.",status=200 , mimetype='application/json')


# SHORT
@app.route('/sortDescending',methods=['GET'])
def sortDescending():
    # check user 
    
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
     # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
   
    choice = data["choice"]

    if  choice == '0':
         users_reservations = list(reservations.find({"name" :currentUser}).sort("time", pymongo.DESCENDING))
         if users_reservations == 0 :
             return Response("You don't have any reservations.",status=404,mimetype="application/json")
         else:
             return Response(f"Your resevations: \n {users_reservations}", status=200 , mimetype='application/json')
    else:
        users_reservations = list(reservations.find({"name" :currentUser}).sort("time", pymongo.ASCENDING))
        if users_reservations == 0 :
             return Response("You don't have any reservations.",status=404,mimetype="application/json")
        else:
             return Response(f"Your resevations: \n {users_reservations}", status=200 , mimetype='application/json')

# DEN leitourgei
# freeze account
@app.route('/freeze',methods=['POST','GET'])
def freeze():
    # check user 
    global random_no
    global user_category
    if user_category == "admin" :
        return Response("Admins Cannot access this menu",status=401,mimetype="application/json")
     # check data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    
    # change the user_catagory to freeze

    user_category =  {"user_category":'freeze'}
    
    no = random.sample(range(0, 9), 12)
    random_no = {"random_no":'no'}
    return Response(f"If you want to unfreeze your account please enter: {random_no}", status=200 , mimetype='application/json')






# creare admin
@app.route('/createAdmin', methods=['POST'])
def create_admin():
        # Request JSON data
     global user_category
     data = None 
     try:
         data = json.loads(request.data)
     except Exception as e:
         return Response("bad json content",status=500,mimetype='application/json') 
     if data == None:
         return Response("bad request",status=500,mimetype='application/json')
     if not "email" in data or not "name" in data or not "password" in data:
         return Response("Information incomplete",status=500,mimetype="application/json") 
        

     if not(users.find_one({"email":data["email"]})) and not(users.find_one({"name":data["name"]})) :
	        # update user_category for admin
         user_category = {"user_category":'admin'}
         data.update(user_category)
         users.insert_one(data) # add user
         return Response("User was added.\n", mimetype='application/json', status=200) 
     else: # if user already in database 
         return Response("A user with this information already exists\n", mimetype='application/json', status=400) 



# add flight - admin
@app.route('/addFlight', methods=['POST','GET'])
def addFlight():
    
    # check user 
    if user_category == 'simple user' :
        return Response("Cannot access this menu",status=401,mimetype="application/json")
    elif user_category == 'admin' :
        
        # check info
        
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')

        if not "departure_destination" in data or not "arrival_destination" in data or not "departure_date" in data or not "departure_time" in data or not "duration" in data or not "flight_id" in data  :
            return Response("Information incomplete",status=500,mimetype="application/json")
        
        # import data
        newFlight ={'departure_destination':data["departure_destination"], 'arrival_destination':data["arrival_destination"], 'duration':data["duration"], 'tickets':data["tickets"], 'flight_id':data["flight_id"], 'departure_date':data["departure_date"], 'departure_time':data["departure_time"]} 
        flights.insert_one(newFlight)

        return Response("Flight added.",status=201 , mimetype='application/json')





# delete flight - admin
@app.route('/deleteFlight', methods=['POST','GET'])
def deleteFlight():

    # check user 
   global user_category
   if user_category == "simple user" :
        return Response("Cannot access this menu",status=401,mimetype="application/json")
   elif user_category == "admin" :
  # check data
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "flight_id" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        flights.delete_one({"flight_id": data["flight_id"]})
       
        return Response("flight deleted.",status=200 , mimetype='application/json')


      


# Update flight
@app.route('/updateFlight', methods=['POST','GET'])
def updateFlight():

      # check user 

    global user_category
    if user_category == "simple user" :
        return Response("Cannot access this menu",status=401,mimetype="application/json")
    elif user_category == "admin" :
       # check data
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("bad json content",status=500,mimetype='application/json')
        if data == None:
            return Response("bad request",status=500,mimetype='application/json')
        if not "flight_id" in data or not "newFlight_id" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")


        flight = flights.find_one({"flight_id" : data["flight_id"]})

        id = str(data["newFlight_id"])


        if len(id) <= 0:
            return Response("Wrong id",status=500,mimetype="application/json")
        elif not flight :
            return Response("Flight can not be found",status=500,mimetype="application/json")
        elif int(flight["tickets"]) !=220:
            return Response("Flight can not be changed, there is a reservation.",status=500,mimetype="application/json")
        else:
            flights.update_one({"flight_id":data['flight_id']},{"$set":{"flight_id":data["newFlight_id"]}})    #kanei update tin flight_id me tin id pou edwse o xristis
            return Response("Flight updated.", status=200 , mimetype='application/json')



      




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
