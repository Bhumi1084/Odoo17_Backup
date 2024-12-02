import xmlrpc.client
import json

# Odoo Connection Details
url = 'http://localhost:8069'
db = 'odoo_map'
username = 'odoo_map'
password = 'odoo_map'

# Connect to Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# JSON File Path
json_file_path = "/Users/apple/Desktop/API/map.json"

# Read JSON Data
try:
    with open(json_file_path, 'r') as file:
        contacts = json.load(file)
except Exception as e:
    print(f"Failed to read JSON file: {e}")
    exit()

# Add or Update Contacts
for contact in contacts:
    name = contact.get("name")
    age = contact.get("age")
    latitude = contact.get("latitude")
    longitude = contact.get("longitude")

    if not name or not age:
        print(f"Skipping invalid entry: {contact}")
        continue

    # Check if the contact already exists
    existing_contact = models.execute_kw(
        db,
        uid,
        password,
        'ajs.contact',
        'search',
        [[('age', '=', age)]]
    )

    if existing_contact:
        # Update existing record
        models.execute_kw(
            db,
            uid,
            password,
            'ajs.contact',
            'write',
            [existing_contact, {'name': name, 'age': age, 'latitude': latitude, 'longitude': longitude}]
        )
        print(f"Updated contact: {name} ({age})")
    else:
        # Create a new record
        models.execute_kw(
            db,
            uid,
            password,
            'ajs.contact',
            'create',
            [{'name': name, 'age': age, 'latitude': latitude, 'longitude': longitude}]
        )
        print(f"Created contact: {name} ({age}, {latitude}, {longitude})")
