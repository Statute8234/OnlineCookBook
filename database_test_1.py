from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.neuraldb
users = db.users

"""password = "test"
Username, Email, Full_Name = "admin", "admin@gmail.com", "Admin name"
user_data = {'Username': Username, 'Email': Email, 'Full Name': Full_Name, 'Password': password}
users.insert_one(user_data)"""

cursor = users.find()
for user in cursor:
    print(user)

print("Done")
