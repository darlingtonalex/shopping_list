from google.cloud import datastore
#Import google cloud libraries

datastore_client = datastore.Client.from_service_account_json('service_account.json')
#Instantiate a client

kind = 'userid'
name =  'sampletask3'

task_key = datastore_client.key(kind, name)

def addItem():

	item = datastore.Entity(key=task_key)
	item['itemid'] = 123456
	item['itemname'] = u"Bread"

	datastore_client.put(item)

	print('Saved {}: {}'.format(item.key.name, item['itemid']))



def overwrite():
	overwriteItem = datastore.Entity(key=task_key)
	overwriteItem['itemid'] = 654321
	overwriteItem['itemname'] = u"Fish"
	datastore_client.put(overwriteItem)
	print ("Overwrite Complete")


def retrieve():
	query = datastore_client.query(kind='userid')
	print query
retrieve()
