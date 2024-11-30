import xmlrpc.client
import base64

url = 'http://localhost:8069'
db = 'testdemo'
username = 'testdemo'
password = 'testdemo'


# SHOW THE DETAILS OF SERVER VERSION
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
print("version = ", version)


# UID AUTHENTICATION
uid = common.authenticate(db, username, password, {})
print("uid = ", uid)


# Import The Model (Required)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# LIST RECORD OR FATCH THE RECORDS
list_record = models.execute_kw(db, uid, password, 'product.template', 'search', [[]])		# fatch all records
print("List record = ", list_record)

list_offset_record = models.execute_kw(db, uid, password, 'product.template', 'search', [[]], {'offset': 10, 'limit': 10})	#fatch only offset and limited record
print("List offset record = ", list_offset_record)

list_record_count = models.execute_kw(db, uid, password, 'product.template', 'search_count', [[]])		# count the records
print("List record count = ", list_record_count)

product_offset_record = models.execute_kw(db, uid, password, 'product.template', 'read', [list_offset_record], {'fields': ['id', 'name']})	#show the id and name of offset and limit data
print("Product offset record = ", product_offset_record)

for product in product_offset_record:
	print(product)


# SEARCH AND READ METHOD
search_read_method = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 10})
print("Search and read method = ", search_read_method)

for search_read in search_read_method:
	print(search_read)


# CREATE METHOD
with open("/Users/apple/Desktop/images/maggi.jpeg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

new_product = models.execute_kw(db, uid, password, 'product.template', 'create', 
	[{'name': "Vage Meegi", 'list_price': "70", 'image_1920': image_data}])
print("Record Created....!",new_product)

# ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[]], {'limit': 1})
# record = models.execute_kw(db, uid, password, 'product.template', 'read', [9], {'fields': ['name', 'image_1920']})
# print(record)