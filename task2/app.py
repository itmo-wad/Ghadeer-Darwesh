from flask import Flask, render_template , request
app = Flask(__name__)


@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')

#app.add_url_rule('/', 'hello' , hello_world)   


if __name__ == '__main__':
    #app.run(debug = True,use_reloader=False)
    #app.run(host='127.0.0.1',port='5000',debug = True,use_reloader=False)
    app.run(threaded=True, port='5000')

