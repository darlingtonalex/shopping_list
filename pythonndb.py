from google.appengine.ext import ndb
import time



class Shopping(ndb.Model):
    """Models an individual Shopping item."""
    userid = ndb.StringProperty()
    item= ndb.StringProperty()


def createnewitem(userid, item):
        listrow=Shopping(userid=userid,item=item)
        key=listrow.put()
        return key

def getitembyid(itemid):
        return Shopping.get_by_id(itemid)

def getallitemsforuser(userid):
        query = Shopping.query(Shopping.userid == userid)
        return query.fetch()

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

def deleteallitems(ndbresultset):
        for i in ndbresultset:
                i.key.delete()
        return None

def deleteitembyid(itemid):
        item = getitembyid(itemid)
	item.key.delete()
	return None


