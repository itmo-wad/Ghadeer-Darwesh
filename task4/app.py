from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbotdb"]
users = db["users"]
users.create_index("username")


app = Flask(__name__)


#secret key for the session
app.secret_key = "super secret key"

    
def add_user_to_db(username,password):
      users.insert({
            "username": username,
            "password": password
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

        
@app.route('/', methods=['Get','POST'])
@app.route('/cabinet', methods=['Get','POST'])
def index():
    
    #check if the user logged in, if not go back to login html
      if not session.get('logged_in'):
          return render_template('login.html')
      
      else:
        msg=''
        
        
        if request.method == 'POST':
              getdata=''
             
            # if the post doesn't include new_message it means that it redirected from login page and no need to process data
              if "new_message" not in request.form :
                  return render_template('cabinet.html')
                    
              #get the new message and the all messages from the request
              getdata = request.form.get("new_message")
              msg = request.form.get("messages")
              user = 'Me : '+ getdata + '\n'
              
              if getdata=='clear':
                  msg = ''
                  return render_template('index.html',dialog=msg)
              
              msg = msg + user
              
              #dic with conversation
              keywords = {
                  
                  'Oh, Hi.\n     How are you doing?':['.*hello.*','^hi$','^hey$','.*good morning.*','.*good afternoon.*','.*good evening.*'],
                  'I am doing right.': ['.*how are you.*','.*you doing.*','.*about you.*','.*and you.*'],
                  'My name is George.\n     Nice to meet you)':['.*your name.*'],
                  'Glad to here that.':['.*good.*','.*fine.*','.*all right.*','.*well.*'],
                  'Any time.':['.*thank.*'],
                  'Why you don\'t see your phone?!':['.*weather.*','.*time.*'],
                  'Sorry, to here that.\n     Maybe you need a break)':['.*problem.*','.*terrible.*','.*bad.*','.*awful.*'],
                  'It\'s ok, let\'s ask google)':['.*don\'t know.*','^no&'],
                  'I was created at the moment you opened this conversation.\n     Thank you)':['.*birth.*','.*born.*'],
                  'I love programming)':['.*favorite.*','.*like.*'],
                  'Goodbye, have a nice day)':['.*bye.*','.*good night.*'],
                  'Sorry, You aren\'t talking with Alice!!':['.*\?.*']
    
               }
              
              found = 0
              bot = 'Bot: '
              
              #search in the dic for the new msg
              for key,value in keywords.items():
                  rr = re.compile('|'.join(value),re.IGNORECASE)
                  if re.search(rr, getdata):
                      bot = bot + key + '\n'
                      found = 1
                      break
                  
              if found == 0 :
                     bot = bot+ 'Mmmm...\n     OK)\n'
                     
              msg = msg + bot + '\n'         
        return render_template('cabinet.html',dialog=msg)
        
          
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    
    #if  method='GET' it comes from log out
    if request.method=='GET':
        session['logged_in'] = False
        return index()  
    
    else:
       #if email not exist it is from login page, else from reg page
        username = request.form.get('username')
        password = request.form.get('password')
        if "email" not in request.form :
                if check_user_in_db(username):
                    if check_pass_in_db(username, password):
                        session['logged_in'] = True
                    else :
                        flash('Wrong Password!')
                else:
                    flash('User not exsit!!')
                return index()    
            
        else:
       
             if check_user_in_db(username) :
                     flash('Username aleady exists!')
                     print(username+"   "+password)
                     session['logged_in'] = False
                     return do_reg()
             else:
                 add_user_to_db(username, password)
                 session['logged_in'] = False
                 return index()
                 
                        
                    
#execute index function after set the session value
    #return index()
 
@app.route('/register')
def do_reg():
    return render_template('reg.html')    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
     
@app.route('/static/<image_name>')
def index2(image_name):
       return send_from_directory('static/img',image_name)
       

@app.route('/static/<path:path>')
def index3(path):
     return app.send_static_file(path)

  
if __name__ == '__main__':
    
    app.run( port='5000',threaded=True)

