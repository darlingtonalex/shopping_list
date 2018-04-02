from google.appengine.ext import ndb
import time
#We are using the nbd database library


class Shopping(ndb.Model):
    #Models an individual Shopping item
    userid = ndb.StringProperty()
    item= ndb.StringProperty()



def createnewitem(userid, item):
        listrow=Shopping(userid=userid,item=item)
        key=listrow.put()
        return key
	#Creates a new item 

def getitembyid(itemid):
        return Shopping.get_by_id(itemid)
	#gets an item by its id

def getallitemsforuser(userid):
        query = Shopping.query(Shopping.userid == userid)
        return query.fetch()
	#gets all items for a user

def updateitembyid(itemid,item):
        listitem=getitembyid(itemid)
        listitem.item=item
        return listitem.put()

def shoppingaslist(ndbresultset):
        shoppinglist=list()
        listitem=dict()
        for i in ndbresultset:
                listitem['itemid']=int(i.key.id())
                listitem['userid']=i.userid
                listitem['item']=i.item
                shoppinglist.append(listitem.copy())
        return shoppinglist
	#passes through the data line by line and returns it as a list

def deleteallitems(ndbresultset):
        for i in ndbresultset:
                i.key.delete()
        return None
	#Passes through the data and deletes each line

def deleteitembyid(itemid):
        item = getitembyid(itemid)
	item.key.delete()
	return None
	#Locates and deletes an item 


