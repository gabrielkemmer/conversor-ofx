import requests
from pymongo import MongoClient
import schedule
import time
from api_whm import *

def update_active_users():
    
    active = list_suspended_emails(get_accounts_list())[1]
    inactive = list_suspended_emails(get_accounts_list())[0]

    # Connect to MongoDB and insert/update the documents
    client = MongoClient('mongodb+srv://gabrielkemmer:Araujo35@cluster0.yxrnwy9.mongodb.net/?retryWrites=true&w=majority')  # Update with your MongoDB connection URI
    db = client['renato']
    users_collection = db['users']  # Replace with your MongoDB collection name

    # Upsert active users into MongoDB collection
    for email in active:
        check_email = users_collection.find_one({'email': email})
        if check_email:
            users_collection.update_one(
                {'email': email},  # Replace '_id' with the unique identifier field of your documents
                {'$set': {'status': 'active'}}
            )

    for email in inactive:
        check_email = users_collection.find_one({'email': email})
        if check_email:
            users_collection.update_one(
                {'email': email},  # Replace '_id' with the unique identifier field of your documents
                {'$set': {'status': 'inactive'}}
            )

    for email in active:
        check_email = users_collection.find_one({'username': email})
        if check_email:
            users_collection.update_one(
                {'username': email},  # Replace '_id' with the unique identifier field of your documents
                {'$set': {'status': 'active'}}
            )

    for email in inactive:
        check_email = users_collection.find_one({'username': email})
        if check_email:
            users_collection.update_one(
                {'username': email},  # Replace '_id' with the unique identifier field of your documents
                {'$set': {'status': 'inactive'}}
            )

schedule.every().day.at("01:00").do(update_active_users)

while True:
    schedule.run_pending()
    time.sleep(1)
