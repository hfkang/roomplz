import pickle,datetime
from flask import Flask,render_template,request,redirect,url_for,make_response
app = Flask(__name__)
app.debug = True

@app.route('/francis')
def frank():
    return str(environ)

def room_plz(b,d,t):
    building = b
    time = t  
    response = [] 
    with open(b+"_organized",'rb') as f:
        availability = pickle.load(f)
    if time>=7 and time <= 22:
        response = availability[d][time-7]
    return response #response is a dictionary whose keys are the room numbers, and values are the duration 

@app.route('/auth',methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        return render_template('login.html') 
    else:
        #process login data
        if request.form['pswd'] == 'potato salad':
            #successful authentication 
            resp = app.make_response(redirect('/'))
            resp.set_cookie('auth',domain='.toastedsesa.me',value='potato horse banana orange sloth')
            return resp
        else:
            return render_template('login.html')    

@app.route('/',methods=['GET'])
def check_auth():
    
    if not ("auth" in request.cookies and request.cookies['auth'] == 'potato horse banana orange sloth'):
        return redirect(url_for('auth'))
    
    q_s = request.query_string.decode('utf-8')
    ct = datetime.datetime.now() 
    time = ct.hour  
    day = ct.weekday() 
    b = 'BA'
    if q_s == "GB":
        b = "GB"
    if q_s == "SF":
        b = "SF" 
    if q_s == "TEST":
        b = "BA"
        day = 1
        time = 12
     
    ts = ct.strftime("%A, %B, %d %I:%M%p")
    rooms1 = room_plz(b,day,time)
    rooms2 = room_plz(b,day,time+1)
    return render_template('layout.html',b=b,ts=ts,rooms1=rooms1,rooms2=rooms2)

if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)
