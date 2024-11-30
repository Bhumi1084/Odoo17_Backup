import xmlrpc.client

url = 'http://localhost:8069'
db = 'testdemo'
username = 'testdemo'
password = 'testdemo'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#show the Odoo Version information (optional) 
#print ("version info = ",common.version()) 


# AUTHENTICATION
uid = common.authenticate(db, username, password, {})
if uid:
	print("------------------------\n")
	print("Authentication Success")
	

	# SEARCH METHOD
	models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
	partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
	#partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'offset': 1, 'limit': 5})
	#partners = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
	partners_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])  #search count method
	print("------------------------\n")
	print("partners = ", partners)
	print("partners_count = ", partners_count)


	# READ METHOD
	partner_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'name', 'country_id', 'comment']})
	print("------------------------\n")
	print("partner_rec = ", partner_rec)


	# SEARCH READ METHOD
	partner_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]], 
		{'fields': ['id', 'name', 'country_id', 'comment']})
	print("------------------------\n")
	print("partner_rec2 = ", partner_rec2)


	# CREATE METHOD
	# vals = {
	# 	'name': "odoo Mates External API",
	# 	'email': "odoomates@gmail.com"
	# }
	# created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
	# print("------------------------\n")
	# print("created_id = ", created_id)


	# WRITE METHOD
	# this method are used to write or update data
	#models.execute_kw(db, uid, password, 'res.partner', 'write', [[11], {'phone': "1234567890"}])
	#models.execute_kw(db, uid, password, 'res.partner', 'write', [[11], {'mobile': "9825362494", 'phone': "9926374562"}])


	# DELETE METHOD
	#models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[12]])		#delete record using id
	partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'odoomates@gmail.com']]])
	models.execute_kw(db, uid, password, 'res.partner', 'unlink', [partners])		#delete record using email

else:
	print("------------------------\n")
	print("Authentication Failed")