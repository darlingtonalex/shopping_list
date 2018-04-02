
from pythonndb import createnewitem, getitembyid, getallitemsforuser, updateitembyid, shoppingaslist, deleteallitems, deleteitembyid
#importing database functions from pythonndb.py
from flask import Flask, request, make_response
from flask import render_template
import json
import time
import urllib2
#Importing necessary libraries

app =  Flask(__name__)

@app.route('/login.html')
def login():
        return render_template('login.html')
#renders the login page template

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
#authorise page
#checks for valid login and sets cookie

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
#Checks for valid user token and uses urllib2 to retrieve relevant user information from a user's URL


def loadlist(filename):
      data = json.load(open(filename))
      return data
#Loads data from file
@app.route('/', methods= ['GET','POST'])
def main():

 	if 'session_token' in request.cookies:
        	print request.cookies['session_token']
        	try:
			token, userid, username, authorised = checkTokenInfo( request.cookies['session_token'] )
    		except: 
			authorised=False
	#Checks for the existence of a token and attempts to validate it using the checkTokenInfo function
	else:
        	print "not authenticated"
        	authorised=False

    	if not authorised:
        	return "<p>Please Login!</p><a href=\"/login.html\">Login Page</a>"
	#Redirects to login page if token is not valid

    	varList=[userid,username]
	print userid
	userName = str(username)
	edititem = -1
	print request
	if request.method=='POST':
        	if (request.form["Action"] == "Delete"):
			print ("Delete Request")
			idToDelete = int(request.form["Id"])
			deleteitembyid(idToDelete)
			#Calls the deleteitembyid function on the relevant item to delete it
		if (request.form["Action"] == "Edit"):
			print ("Edit Request")
			idToEdit = request.form["Id"]
			print idToEdit
			edititem = int(idToEdit)
			#Gets the id of the item that the user has selected to edit as an int
		if (request.form["Action"] == "Update"):
			print ("Update Request")
			idToUpdate = request.form["Id"]
			print idToUpdate
			valueToUpdate = request.form["EditItem"]
			print valueToUpdate
			updateitembyid(int(idToUpdate), valueToUpdate)
			#Updates a given item using the updateitembyid function
		if (request.form["Action"] == "Add"):
			itemToAdd = request.form["itemToAdd"]
			print itemToAdd
			createnewitem(userid, itemToAdd)
			#Calls the createnewitem function based on the userid and inputed text from the user

		if (request.form["Action"] == "deleteAll"):
			allItems = getallitemsforuser(userid)
			deleteallitems(allItems)
			#Deletes all items using the deleteallitems function
	time.sleep(0.2)
	shoppingList = shoppingaslist(getallitemsforuser(userid))
	#Redisplays a shopping list after changes
	print shoppingList
	return render_template("template1.html", shoppingList = shoppingList, userName=userName, edititem=edititem, varList=varList)
	#Renders the shopping list page with the necessary variables. These can now be called directly in the template files using flask
