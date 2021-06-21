from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
from bson import json_util
import pymongo
from collections import defaultdict
# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/', connect=False)

# Choose database
db = client['InfoSys']

# Choose collections
products = db['Products']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

UserCart={}
TempCart=[]
UserCart.update({"cart":TempCart})
UserCart.update({"cart_cost":0})

def create_session(email):
  user_uuid = str(uuid.uuid1())
  users_sessions[user_uuid] = (email, time.time())
  return user_uuid  

def is_session_valid(user_uuid):
  return user_uuid in users_sessions

 
# Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "name" in data or not "password" in data or not "email" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")

  if users.find({"email": data['email']}).count()==0 :
    users.insert_one({"name": data['name'], "password": data['password'], "email":data['email'], "category":"user"})
    return Response("The user with the email " +data['email']+ " was added to MongoDB", status=200 , mimetype='application/json')
  else:
    return Response("A user with the given email already exists",status=400 , mimetype='application/json')

#Δημιουργια Διαχειριστη
@app.route('/createAdmin', methods=['POST'])
def create_Admin():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "name" in data or not "password" in data or not "email" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")

  if users.find({"email": data['email']}).count()==0 :
    users.insert_one({"name": data['name'], "password": data['password'], "email":data['email'], "category":"admin"})
    return Response("The admin with the email: " +data['email']+ " was added to the MongoDB", status=200 , mimetype='application/json')
  else:
    return Response("A user with the given email already exists",status=400 , mimetype='application/json')

#Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
  # Request JSON data
  data = None 
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data or not "password" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")


  # Έλεγχος δεδομένων email
    
  # Αν η αυθεντικοποίηση είναι επιτυχής. 
  
  if users.find({"email": data['email'] , "password": data['password']}).count()!=0: 
    user_uuid=create_session(data['email'])
    res = {"uuid": user_uuid, "email": data['email']}
    return Response(json.dumps(res), mimetype='application/json', status=200) 
  else:
    # Μήνυμα λάθους 
    return Response("Invalid User email. Please register to our system again.",mimetype='application/json',status=400) 
  
# ΕΡΩΤΗΜΑ 3: Επιστροφή product βαση name η id η category 
@app.route('/getProduct', methods=['GET'])
def get_Product():
  # Request JSON data
  data = None 
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if (not "name" in data and "category" in data and "_id" in data) or ("name" in data and not "category" in data and "_id" in data) or ("name" in data and "category" in data and not "_id" in data)   :
    return Response("Information incomplete",status=500,mimetype="application/json")

    
  uuid = request.headers.get('authorization')
   
  if is_session_valid(uuid):
    if "name" in data:
      para=products.find({"name":data['name']}).sort([("category", pymongo.ASCENDING)])
      product=json.loads(json_util.dumps(para))
      if products.find({"name":data['name']}).count()!=0:
        return Response(json.dumps(product), mimetype='application/json', status=200)
      else:
        return Response("There is no product with that name" , status=400, mimetype="application/json")
    elif "category" in data:
      para=products.find({"category":data['category']}).sort([("price", pymongo.ASCENDING)])
      product=json.loads(json_util.dumps(para))
      if products.find({"category":data['category']}).count()!=0:
        return Response(json.dumps(product), mimetype='application/json', status=200)
      else:
        return Response("There is no product in that category" , status=400, mimetype="application/json")
    elif "_id" in data:
      para=products.find({"_id":data['_id']})
      product=json.loads(json_util.dumps(para))
      if products.find({"_id":data['_id']}).count()!=0:
        return Response(json.dumps(product), mimetype='application/json', status=200)
      else:
        return Response("There is no product with that ID" , status=400, mimetype="application/json")  
  else:
    return Response("Non authenticated user" , status=401, mimetype="application/json")  

#Προσθηκη προιοντων στο καλαθι του χρηστη 
@app.route('/AddtoCart', methods=['GET'])
def Add_to_Cart():
  # Request JSON data
  global UserCart
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "_id" in data or not "stock" in data or not "email" in data:
    return Response("Information incomplete",status=500,mimetype="application/json") 

  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    product=products.find_one({"_id":data['_id']})
    if products.find({"_id":data['_id']}).count()==0:
      return Response("no products wih that id were found", status=400, mimetype='application/json')
    else:
      if product in UserCart['cart']:
        return Response("You have already added that product to your cart", status=401, mimetype='application/json')
      elif product not in UserCart['cart'] :
        if data['stock']<=product['stock']:
          UserCart['cart'].append(product)
          total_cost=0
          for prods in UserCart['cart']:
            total_cost=total_cost+prods['price']*data['stock']
          UserCart.update({"cart_cost":total_cost})
          users.update_one({"email": data['email']} , {'$set' : { "Order_History" : UserCart['cart']}})
          return Response(json.dumps(UserCart), status=200, mimetype='application/json')
        else:
          return Response("not enough stock", status=401, mimetype='application/json')
  else:
    return Response("non authenticated user", status=401, mimetype='application/json')   

#Επιστροφη Καλαθιου στον χρηστη
@app.route('/ShowCart', methods=['GET'])
def Show_Cart():
  # Request JSON data
  global UserCart
  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    return Response("Your Cart: " + json.dumps(UserCart), status=200, mimetype='application/json')
  else:
    return Response("non authenticated user", status=401, mimetype='application/json')  


#Διαγραφη προιοντων απο το καλαθι του χρηστη 
@app.route('/DeleteFromCart', methods=['GET'])
def Delete_From_Cart():
  # Request JSON data
  global UserCart
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "_id" in data:
    return Response("Information incomplete",status=500,mimetype="application/json") 

  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    product=products.find_one({"_id":data['_id']})
    if products.find({"_id":data['_id']}).count()==0:
      return Response("no products with that id were found", status=400, mimetype='application/json')
    else:
      if product in UserCart['cart']:
        updated_cost=UserCart['cart_cost']-product['price']
        UserCart['cart'].remove(product)
        UserCart.update({"cart_cost":updated_cost})
        return Response("Your cart after the deletion of the required product: " + json.dumps(UserCart), status=200, mimetype='application/json')
      else:
        return Response("You have not added that product to your cart", status=401, mimetype='application/json')
  else:
    return Response("non authenticated user", status=401, mimetype='application/json')  


#Aγορα προιοντων στο καλαθι
@app.route('/Checkout', methods=['GET'])
def Pay_Up():
  # Request JSON data
  global UserCart

  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "card" in data:
    return Response("Information incomplete",status=500,mimetype="application/json") 


  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    card_string=str(data['card'])
    if UserCart['cart']:
      if len(card_string)==16: 
        rec_cost=UserCart['cart_cost']
        UserCart.clear()
        return Response("Your Card has been accepted and the total cost of your order is : " + json.dumps(rec_cost), status=200, mimetype='application/json')
      else:
        return Response("Your card is invalid and therefore declined") 
    else:
      return Response("Your cart is empty")
  else:
    return Response("non authenticated user", status=401, mimetype='application/json')  

#Aγορα προιοντων στο καλαθι
@app.route('/ShowOrderHistory', methods=['GET'])
def Order_History():
  # Request JSON data
  global UserCart

  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data:
    return Response("Information incomplete",status=500,mimetype="application/json") 


  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    para=users.find_one({"email":data['email']})
    user=json.loads(json_util.dumps(para))
    if users.find({"$and":[{"email" : data['email']}, {"Order_History": { "$exists": True }}]}).count()!=0:
     return Response("Your Order History : " + json.dumps(user['Order_History']), status=200, mimetype='application/json')
    else:
      return Response("this user has not made any orders yet")
  else:
    return Response("non authenticated user", status=401, mimetype='application/json')  

# Διαγραφη λογαριασμου χρήστη
@app.route('/DeleteUser', methods=['DELETE'])
def delete_user():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")
  

  uuid = request.headers.get('authorization')
  if is_session_valid(uuid):
    if users.find({"email": data['email']}).count()!=0 :
      users.delete_one({"email":data['email']})
      return Response("The user with the email " +data['email']+ " was deleted from MongoDB", status=200 , mimetype='application/json')
    else:
      return Response("A user with the given email does not exist in the database",status=400 , mimetype='application/json')
  else:
    return Response("Unauthorized User.")

# Δημιουργία προιοντος
@app.route('/createProduct', methods=['POST'])
def create_prod():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data or not "name" in data or not "price" in data or not  "description" in data or not "category" in data or not "stock" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")

  
  if users.find({"email": data['email'] , "category":"admin"}).count()!=0:
    if products.find({"name": data['name'], "price": data['price'], "description":data['description'], "category":data['category'],"stock":data['stock']}).count()==0: 
      products.insert_one({"name": data['name'], "price": data['price'], "description":data['description'], "category":data['category'],"stock":data['stock']})
      return Response("The product inserted by the admin " +data['email']+ " was added to MongoDB", status=200 , mimetype='application/json')
    else:
      return Response("This product already exists in the database.") 
  else:
    return Response("This user is not an admin therefore he has no authorized access.",status=400 , mimetype='application/json')

#Διαγραφη προιοντος
@app.route('/deleteProduct', methods=['DELETE'])
def delete_prod():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data or not "_id" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")

  if users.find({"email": data['email'] , "category":"admin"}).count()!=0:
    if products.find({"_id":data['_id']}).count()!=0: 
      products.delete_one({"_id":data['_id']})
      return Response("The product selected by the admin " +data['email']+ " was deleted from MongoDB", status=200 , mimetype='application/json')
    else:
      return Response("This product does not exist in the database.") 
  else:
    return Response("This user is not an admin therefore he has no authorized access.",status=400 , mimetype='application/json')


#Ενημερωση προιοντος
@app.route('/updateProduct', methods=['PATCH'])
def update_prod():
  # Request JSON data
  data = None
  try:
    data = json.loads(request.data)
  except Exception as e:
    return Response("bad json content",status=500,mimetype='application/json')
  if data == None:
    return Response("bad request",status=500,mimetype='application/json')
  if not "email" in data or not "_id" in data:
    return Response("Information incomplete",status=500,mimetype="application/json")

  if users.find({"email": data['email'] , "category":"admin"}).count()!=0:
    if products.find({"_id":data['_id']}).count()!=0: 
    
      if "name" in data and not "price" in data and not "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       return Response("The name of the product has been updated", status=200 , mimetype='application/json')
      elif not "name" in data and "price" in data and not "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       return Response("The price of the product has been updated", status=200 , mimetype='application/json')
      elif not "name" in data and not "price" in data and "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       return Response("The description of the product has been updated", status=200 , mimetype='application/json')
      elif not "name" in data and not "price" in data and not "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       return Response("The stock of the product has been updated", status=200 , mimetype='application/json')
      elif "name" in data and "price" in data and not "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       return Response("The name and price of the product have been updated", status=200 , mimetype='application/json')
      elif "name" in data and not "price" in data and "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       return Response("The name and description of the product have been updated", status=200 , mimetype='application/json')
      elif "name" in data and not "price" in data and not "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       return Response("The name and stock of the product have been updated", status=200 , mimetype='application/json')
      elif not "name" in data and "price" in data and "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       return Response("The price and description of the product have been updated", status=200 , mimetype='application/json')
      elif not "name" in data and "price" in data and not "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       return Response("The price and stock of the product have been updated", status=200 , mimetype='application/json')
      elif not "name" in data and not "price" in data and "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       return Response("The description and stock of the product have been updated", status=200 , mimetype='application/json')
      elif  "name" in data and  "price" in data and "description" in data and not "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       return Response("The name, price and description of the product have been updated", status=200 , mimetype='application/json')
      elif  "name" in data and  "price" in data and not "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       return Response("The name, price and stock of the product have been updated", status=200 , mimetype='application/json')
      elif  "name" in data and not "price" in data and "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       return Response("The name, price and description of the product have been updated", status=200 , mimetype='application/json')
      elif not "name" in data and "price" in data and "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       return Response("The stock, price and description of the product have been updated", status=200 , mimetype='application/json')
      elif "name" in data and "price" in data and "description" in data and "stock" in data:
       products.update_one({"_id": data['_id']} , {'$set' : { "stock" : data['stock']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "description" : data['description']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "price" : data['price']}})
       products.update_one({"_id": data['_id']} , {'$set' : { "name" : data['name']}})
       return Response("The stock, price, name and description of the product have been updated", status=200 , mimetype='application/json')
    else:
      return Response("This product does not exist in the database.") 
  else:
    return Response("This user is not an admin therefore he has no authorized access.",status=400 , mimetype='application/json')






# Εκτέλεση flask service σε debug mode, στην port 5000. 

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)