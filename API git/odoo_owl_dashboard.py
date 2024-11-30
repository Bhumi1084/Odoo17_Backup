import xmlrpc.client
import base64
import json
import requests

url = 'http://localhost:8069'
db = 'odoo_owl_dashboard'
username = 'odoo_owl_dashboard'
password = 'odoo_owl_dashboard'


# SHOW THE DETAILS OF SERVER VERSION
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# version = common.version()
# print("version = ", version)


# UID AUTHENTICATION
uid = common.authenticate(db, username, password, {})
# print("uid = ", uid)


# Import The Model (Required)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# LIST RECORD OR FATCH THE RECORDS
# list_record = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])		# fatch all records
# print("List record = ", list_record)

# list_offset_record = models.execute_kw(db, uid, password, 'product.template', 'search', [[]], {'offset': 10, 'limit': 10})	#fatch only offset and limited record
# print("List offset record = ", list_offset_record)

# list_record_count = models.execute_kw(db, uid, password, 'product.template', 'search_count', [[]])		# count the records
# print("List record count = ", list_record_count)

# product_offset_record = models.execute_kw(db, uid, password, 'product.template', 'read', [list_offset_record], {'fields': ['id', 'name']})	#show the id and name of offset and limit data
# print("Product offset record = ", product_offset_record)

# for product in product_offset_record:
# 	print(product)


# SEARCH AND READ METHOD
# search_read_method = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 10})
# print("Search and read method = ", search_read_method)

# for search_read in search_read_method:
# 	print(search_read)


# CREATE METHOD
# with open("/Users/apple/Desktop/images/maggi.jpeg", "rb") as image_file:
#     image_data = base64.b64encode(image_file.read()).decode('utf-8')

# new_product = models.execute_kw(db, uid, password, 'product.template', 'create', 
# 	[{'name': "Vage Meegiii", 'list_price': "70", 'image_1920': image_data}])
# print("Record Created....!",new_product)

# ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]], {'limit': 1})
# record = models.execute_kw(db, uid, password, 'product.template', 'read', [9], {'fields': ['name', 'image_1920']})
# print(record)


# JSON DATA
json_url = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"

response = requests.get(json_url)
if response.status_code != 200:
    print(f"Failed to fetch JSON data: {response.status_code}")
    exit()

countries = response.json()

# Add or Update Country Records
for country in countries:
    name = country.get("name", {}).get("common", "Unknown")
    code = country.get("cca2", "Unknown")  # Country code
    tld = ", ".join(country.get("tld", []))  # Top-level domain (as a string)

    # Fetch flag image (using code to retrieve from a public source)
    flag_url = f"https://flagcdn.com/w320/{code.lower()}.png"
    flag_response = requests.get(flag_url)
    flag = False
    if flag_response.status_code == 200:
        flag = base64.b64encode(flag_response.content).decode('utf-8')  # Store the binary data of the image

    if not name or not tld:
        print(f"Skipping invalid entry: {country}")
        continue

# Check if the country already exists
    existing_country = models.execute_kw(
        db,
        uid,
        password,
        'country.import',
        'search',
        [[('code', '=', code)]]
    )

    if existing_country:
        # Update existing record
        models.execute_kw(
            db,
            uid,
            password,
            'country.import',
            'write',
            [existing_country, {'name': name, 'tld': tld, 'flag': flag}]
        )
        print(f"Updated country: {name} ({tld})")
    else:
        # Create a new record
        models.execute_kw(
            db,
            uid,
            password,
            'country.import',
            'create',
            [{'name': name, 'code': code, 'tld': tld, 'flag': flag}]
        )
        print(f"Created country: {name} ({code}, {tld}, {flag})")



        # try:
        #     # Fetch JSON Data
        #     response = requests.get(json_url)
        #     response.raise_for_status()  # Raise exception for HTTP errors

        #     # Parse JSON Data
        #     countries = response.json()

        #     for country in countries:
        #         # Extract relevant fields from JSON
        #         name = country.get("name", {}).get("common", "Unknown")  # Country name
        #         code = country.get("cca2", "Unknown")  # Country code
        #         tld = ", ".join(country.get("tld", []))  # Top-level domain (as a string)

        #         # Check if the record already exists
        #         existing_country = self.env['country.import'].search([('code', '=', code)])
        #         if existing_country:
        #             # Update existing record
        #             existing_country.write({
        #                 'name': name,
        #                 'tld': tld,
        #             })
        #         else:
        #             # Create new record
        #             self.create({
        #                 'name': name,
        #                 'code': code,
        #                 'tld': tld,
        #             })

        # except requests.exceptions.HTTPError as http_err:
        #     print(f"HTTP error occurred: {http_err}")
        # except requests.exceptions.RequestException as err:
        #     print(f"Error occurred: {err}")