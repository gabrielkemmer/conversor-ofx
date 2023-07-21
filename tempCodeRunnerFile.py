
url = 'https://contabilitools.com.br/whmcs/includes/api.php'
data = {
    'action': 'GetClients',
    'username': 'V3E02x1ZgILbSHoRmVcFyryTtqN4CUDw',
    'password': 'xX2A4DUhfuxU1PGk7p2xdS9SMM5j2wRM',
    'responsetype': 'json',
}

try:
    response = requests.post(url, data=data)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
    else:
        print(f"Request Error: {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")

active = []
inactive = []

for user in response_data['clients']['client']:
    if user['status'] == 'Active':
        active.append(user['email'])
    else:
        inactive.append(user['email'])

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

