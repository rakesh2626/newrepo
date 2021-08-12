import threading
from flask import Flask,request,current_app
from threading import Thread
from flask.ctx import copy_current_request_context
from flask.json import  jsonify
import pymongo
app = Flask(__name__)
client = pymongo.MongoClient('mongodb+srv://rakesh_26:RAKESH@cluster0.dpzwp.mongodb.net/test')
db = client['companys']
mydb = db['cognitivzen']

def getusers():
    users =mydb.find()
    multipleuser = []
    for i in users:
        i.pop('_id')
        multipleuser.append(i)
    return ('welcome'+ str(multipleuser))

def delete(name):
    users = mydb.delete_one({'name':str(name)})
    return jsonify('user deleted sucessfully')

def add():
    json = request.json
    _name = json['name']
    _email= json['email']
    _password = json['password']

    if _name and _email and _password and request.method == 'POST':
        id = mydb.insert({'name':_name,'email':_email,'password':_password})
        response = jsonify('user added sucessfully')
        response.status_code = 200
        return response

def getuser(name):
    user=mydb.find_one({'name':str(name)})
    user.pop('_id')
    return jsonify({'users':user})
    
def put(name):
    _name1 = name
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and _name and request.method=='PUT':

        data = ({'name':_name,'email':_email,'password':_password})
        query = {'name':_name1}
        mydb.update_one(query,{'$set':data})

@app.route("/",methods=['GET','POST','PUT','DELETE'])
def home():
    thread1 = threading.Thread(target=copy_current_request_context(getusers)).start()
    thread2 = threading.Thread(target=copy_current_request_context(add)).start()
    thread3 = threading.Thread(target=copy_current_request_context(put),args=(current_app._get_current_object())).start()
    thread4 = threading.Thread(target=copy_current_request_context(delete),args=(current_app._get_current_object())).start()
    thread5 = threading.Thread(target=copy_current_request_context(getuser),args=(current_app._get_current_object())).start()

    if request.method =='POST':
        adds = add()
        return str(adds)
    elif request.method =='GET':
        status=getusers()
        return str(status)
    elif request.method =='PUT':
        name=input("\n enter the name to update\n")
        putted=put(name)
        return str(putted)
    elif request.method=='GET':
        name=input("\n enter the name to get details")
        getted=getuser(name)
        return str(getted)
    elif request.method=='DELETE':
        name=input("enter details to delete a user")
        deleted=delete(name)
        return deleted
    else:
        return "invalid input"
print(app.url_map)

if __name__ == '__main__':

    app.run(debug=True,threaded = True)