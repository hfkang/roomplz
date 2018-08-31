import json,datetime, boto3
from flask import Flask,render_template,request,redirect,url_for,make_response
from flask_s3 import FlaskS3
from osm import blist


app = Flask(__name__)
app.config['FLASKS3_BUCKET_NAME'] = 'roomplz-assets'
app.config['FLASKS3_BUCKET_DOMAIN'] = 's3-us-west-2.amazonaws.com'
app.config['FLASKS3_FORCE_MIMETYPE'] = True
s3 = FlaskS3(app)


@app.route("/exams")
def examsched():
    return render_template('examsched.html')

def room_plz(b,d,t):

    time = t  
    response = []

    filename = b + "_organized.json"
    filepath = '/tmp/' + filename

    client = boto3.client('s3')
    client.download_file('roomplz-data', filename, filepath)

    with open(filepath,'r') as f:
        availability = json.load(f)

    if time>=7 and time <= 22:
        response = availability[d][time-7]
    return response #response is a dictionary whose keys are the room numbers, and values are the duration 

@app.route('/auth',methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        return render_template('login.html') 
    else:
        #process login data
        if 'pswd' in request.form and request.form['pswd'] == 'potato salad':
            #successful authentication 
            resp = app.make_response(redirect('/'))
            resp.set_cookie('auth',max_age=15000000,value='potato horse banana orange sloth')
            return resp
        else:
            return render_template('login.html')    

def check_auth():
    if not ("auth" in request.cookies and request.cookies['auth'] == 'potato horse banana orange sloth'):
        return redirect(url_for('auth'))



@app.route('/',methods=['GET'])
def home_page():


    if check_auth():
        return check_auth()

    q_s = request.query_string.decode('utf-8')
    ct = datetime.datetime.now() 
    time = ct.hour  
    day = ct.weekday() 
    b = 'BA'
    if q_s in blist:
        b = q_s
    if "TEST" in q_s:
        b = request.args.get('building')
        time = int(request.args.get('time'))
        day = int(request.args.get('day'))
        ct = datetime.datetime(ct.year,ct.month,day,hour = time)
        day = ct.weekday()
     
    ts = ct.strftime("%A, %B, %d %I:%M%p")
    rooms1 = room_plz(b,day,time)
    rooms2 = room_plz(b,day,time+1)

    return render_template('layout.html',b=b,ts=ts,rooms1=rooms1,rooms2=rooms2,blist = blist)

if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)
