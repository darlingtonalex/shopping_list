
from pythonndb import createnewitem, getitembyid, getallitemsforuser, updateitembyid, shoppingaslist, deleteallitems, deleteitembyid
from flask import Flask, request, make_response
from flask import render_template
import json
import time
import urllib2

app =  Flask(__name__)

@app.route('/login.html')
def login():
        return render_template('login.html')

@app.route('/authorise.html', methods=['POST'])
def authorise():
	userid=None
   	username=None
    	response=make_response("")
    	token=request.form['idtoken']
    	print token
    	token, userid, username, authenticated=checkTokenInfo(token)
    	if authenticated:
		print userid, username
        	response.set_cookie('session_token',value=token)

    	return response


def checkTokenInfo(token):
	URL = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+token
	contents = None
	userid = None
	username = None
	contents = json.loads(urllib2.urlopen(str(URL)).read())
	if contents is None:
		return ("not authorised", userid, username, False)
	else:
		return token, contents['sub'], contents['given_name'], True

def loadlist(filename):
      data = json.load(open(filename))
      return data

@app.route('/', methods= ['GET','POST'])
def main():

 	if 'session_token' in request.cookies:
        	print request.cookies['session_token']
        	try:
			token, userid, username, authorised = checkTokenInfo( request.cookies['session_token'] )
    		except: 
			authorised=False
	else:
        	print "not authenticated"
        	authorised=False

    	if not authorised:
        	return "<p>Access Denied</p><a href=\"/login.html\">Try again</a>"

    	varList=[ userid,username ]
#	userid = uint(userid)
	print userid
	testvar = "abcd123"
	listName = "Default List Name"
	edititem = -1
	print request
	if request.method=='POST':
        	if (request.form["Action"] == "Delete"):
			print ("Delete Request")
			idToDelete = int(request.form["Id"])
			deleteitembyid(idToDelete)
		if (request.form["Action"] == "Edit"):
			print ("Edit Request")
			idToEdit = request.form["Id"]
			print idToEdit
			edititem = int(idToEdit)
	#		updateitembyid(1,"Apple")
		if (request.form["Action"] == "Update"):
			print ("Update Request")
			idToUpdate = request.form["Id"]
			print idToUpdate
			valueToUpdate = request.form["EditItem"]
			print valueToUpdate
			updateitembyid(int(idToUpdate), valueToUpdate)
		if (request.form["Action"] == "Add"):
			itemToAdd = request.form["itemToAdd"]
			print itemToAdd
			createnewitem(userid, itemToAdd)
		print "POST Request"
		if (request.form["Action"] == "deleteAll"):
			allItems = getallitemsforuser(userid)
			deleteallitems(allItems)
	time.sleep(0.2)
	shoppingList = shoppingaslist(getallitemsforuser(userid))
	print shoppingList
	return render_template("template1.html", testvar=testvar, shoppingList = shoppingList, listName=listName, edititem=edititem, varList=varList)
