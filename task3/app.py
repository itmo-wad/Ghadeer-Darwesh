from flask import Flask, render_template,request,send_from_directory,session,flash
import re
import os


app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/', methods=['Get','POST'])
@app.route('/cabinet', methods=['Get','POST'])
def index():
      if not session.get('logged_in'):
          return render_template('login.html')
      
      else:
        msg=''
        
        
        if request.method == 'POST':
              getdata=''
             
              if "new_message" not in request.form :
                  return render_template('cabinet.html')
                    
              
              getdata = request.form.get("new_message")
              msg = request.form.get("messages")
              user = 'Me : '+ getdata + '\n'
              
              if getdata=='clear':
                  msg = ''
                  return render_template('index.html',dialog=msg)
              
              msg = msg + user
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
          
          
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        
    else:
        flash('Wrong Username or Password!')
        
    return index()
    
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

