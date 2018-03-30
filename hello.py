from flask import Flask, request
from flask import render_template
import json

app = Flask(__name__)

def loadlist(filename):
      data = json.load(open(filename))
      return data

@app.route('/', methods= ['GET','POST'])
def hello():
	testvar = "abcd123"
	shoppingList = loadlist("store.json")
	listName = "Default List Name"

	if request.method=='POST':
                print request.form

	return render_template("template1.html", testvar=testvar, shoppingList = shoppingList, listName=listName)

	if request.method=='POST':
		print request.form
		
