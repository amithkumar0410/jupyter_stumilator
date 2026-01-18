from flask import Flask, render_template, request,jsonify,redirect,url_for,session
from codebase_py.auth import *
from codebase_py.file_op import op
from codebase_py.run import RunCell
import os
import json

from pymongo import MongoClient
import subprocess
verify=verify()
app = Flask(__name__)
user={"user":None}
app.secret_key = "supersecret"
runobj=None
client = MongoClient("mongodb://localhost:27017/")
db = client["lwnoteb"]
collection= db["user_log"]

@app.route("/",)
def home():
     
     return render_template("login.html",)

@app.route("/get_otp",methods=["POST", "GET"])
def get_otp(): 
    username=request.form['username']
    uid=request.form['_id']
    passw=request.form['passw']
    email=request.form['email']
    
    
    
    check=collection.find_one({"_id":uid})
    if check:
        
        
        
        print("user exits already")
        return render_template("register.html",res="user_name_already_exits . try other ")
        
    else:
        otp=verify.send_mail(email)
        session["user_data"]={"_id":uid,"user":username,"password":passw,"email":email,"otp":otp}
        #print("done")
        return render_template("checkotp.html")
    
@app.route("/register",methods=["POST", "GET"])
def register(): 
        otp=request.form['otp']
        
       
        email=session["user_data"]["email"]
        otp=session["user_data"]["otp"]
        req=verify.verify_otp(email,otp)
        if req==True:
            username=session["user_data"]["_id"]
            session["username"]=username
            path=f"user\\{username}"
            subprocess.run(["mkdir",path],shell=True)
            
            collection.insert_one(session["user_data"])
            return redirect(url_for("open"))
        else:
            return "worng otp"
        print(uid,username,email,passw)
        return "0"
    
    
    
    

  


@app.route("/new_file",methods=["POST", "GET"])
def new_file():
   
    runobj=RunCell(user["user"])
    name=request.args.get("filename")
    op1=op()
    op1.save_data([],[],name,session["username"])
    return redirect(url_for('open_file', filename=name))

 
    
    

@app.route("/call_register")
def call_register():
 
    return render_template("register.html")
    
    

@app.route("/login",methods=["GET", "POST"])
def login():
    username=request.form['username']                      
    passw=request.form["passw"]
    #obj=login.log_reg()
    auth=log_reg()
   
    
    if auth.login(username,passw):
        session["username"]=username
        return redirect(url_for("open"))
        
    else:
        return render_template("login.html",res="user name or password is incorrect")




@app.route("/save_data",methods=["GET","POST"])
def save():
    data=request.get_json()
    
    print("the data is ",data)
    name=data['name']
    inp=data["inp"]
    out=data["out"]
    print("the file name is",name)
    """list1=data.get("inp",[])
    list2=data.get("out",[])
    print("we pass 1")
    list3=data.get("name",[])
    print("we pass 2")
        
    print("we are  at"+list3)"""
    try:
        op1=op()
        op1.save_data(inp,out,name,session["username"])
    except Exception as er:
        print(er)
  
    return jsonify({"satus":"recived"})
    
@app.route("/run_code",methods=["get","post"])
def run_code():
    data=request.args.get("code")
   
    return "1"

@app.route("/open")
def open():
    print("we are here")
    path="user\\"+session["username"]
    print(path)
    x=os.listdir(path)
    x=[y.split(".")[0] for y in x]
    print(x)

    print("hi")
    return render_template("open.html",file=x)
@app.route("/open_file", methods=["POST", "GET"])
def open_file():
    
    a=request.args.get("filename")
    
    
    op1=op()
    inp,out=op1.open(a,session["username"])
   
    return render_template("py_note.html",inp=inp,out=out,file=a)

@app.route("/run_now", methods=["POST"])
def run():
    if "username" not in session:
        return jsonify({"status": "error", "output": "Not logged in!"}), 403

    data = request.get_json()
    code = data.get("code", "")
    user_input = data.get("input", None)

    runobj = RunCell(session["username"])
    result = runobj.run_code_persistent(code, user_input)

    return jsonify(result)




if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",threaded=True,port=8000)