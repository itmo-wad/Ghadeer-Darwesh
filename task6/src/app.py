from flask import Flask, render_template,request,send_from_directory,session,flash,redirect
import re
import os
from pymongo import MongoClient
import random

client = MongoClient('mongodb', 27017)
db = client.wad
#client = pymongo.MongoClient("mongodb://localhost:27017/")
#client = pymongo.MongoClient(os.environ.get('MONGODB_URI', None))
#db = client["wad"]
users = db.users
users.create_index("username")


app = Flask(__name__)

#uplaod dir
app.config['UPLOAD_FOLDER'] = 'static/upload'

#secret key for the session
app.secret_key = "super secret key"

    
def add_user_to_db(username,password):
      users.insert({
            "username": username,
            "password": password,
            "avatar"  : ""
        })
    
def check_user_in_db(username):
    # user = users.find({"username":username})
    user = users.find_one({"username":username})
    if user :        
       
        return True

def check_pass_in_db(username,password):
        user=users.find_one({"username":username})
        if user["password"] == password:
            return True

def update_avatar(username,avatar):
         myquery = { "username": username }
         newvalues = { "$set": { "avatar": avatar } }

         users.update_one(myquery, newvalues)
         return True

def get_avatar(username):
        user=users.find_one({"username":username})
        return user["avatar"] 
            

        
@app.route('/', methods=['Get','POST'])
@app.route('/cabinet', methods=['Get','POST'])
def index():
    
    #check if the user logged in, if not go back to login html
      if not session.get('logged_in'):
           return redirect("/login", code=302)
      
      else:
        username = session.get('username')   
        
        if request.method == 'POST':
            # from login page redirect to cabinet with get
              if request.referrer.endswith('login'):
                  return redirect("/cabinet")
              
              #upload file  
              else:
                if 'file' not in request.files:
                      flash('file not exists')
                      return redirect("/cabinet")
                
                if request.files['file'].filename == "":
                      flash('file name is empty')
                      return redirect("/cabinet")
                  
                ff = request.files['file']
                avatar = os.path.join(app.config['UPLOAD_FOLDER'], ff.filename)
                ff.save(avatar)
                update_avatar(username,avatar)
                flash('Successfully saved')
           
        file = get_avatar(username)                      
        return render_template('cabinet.html',file=file)

@app.route('/uploads/<image_name>')
def upload_file(image_name):
       return send_from_directory(app.config['UPLOAD_FOLDER'],image_name)        
          
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    
    #if  method='GET' it comes from log out or redirected
    if request.method=='GET':
        session['logged_in'] = False
        return render_template('login.html')   
    
    else:
       
        #if email not exist it is from login page, else from reg page
        username = request.form.get('username')
        password = request.form.get('password')
        if "email" not in request.form :
        
                if check_user_in_db(username):
                    if check_pass_in_db(username, password):
                        session['logged_in'] = True
                        session['username'] = username
                        
                    else :
                        flash('Wrong Password!')
                else:
                    flash('User not exsit!!')
                return index()    
            
        else:
       
             if check_user_in_db(username) :
                     flash('Username aleady exists!')
                     session['logged_in'] = False
                     return do_reg()
             else:
                 add_user_to_db(username, password)
                 session['logged_in'] = False
                 return index()

 
@app.route('/register')
def do_reg():
    return render_template('reg.html')    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
     
@app.route('/static/<image_name>')
def index2(image_name):
       return send_from_directory('static/upload',image_name)
       

@app.route('/static/<path:path>')
def index3(path):
     return app.send_static_file(path)

  
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)

