import pickle,datetime
from flask import Flask,render_template,request,redirect,url_for,make_response
app = Flask(__name__)
app.debug = True

@app.route("/R")
@app.route("/r")
@app.route("/RStudio")
@app.route("/rstudio")
@app.route("/stats")
def arr():
    return redirect("http://toastedsesa.me:8787")

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
            resp.set_cookie('auth',max_age=15000000,domain='.toastedsesa.me',value='potato horse banana orange sloth')
            return resp
        else:
            return render_template('login.html')    

def check_auth():
    
    if not ("auth" in request.cookies and request.cookies['auth'] == 'potato horse banana orange sloth'):
        return redirect(url_for('auth'))
    else:
        return None

@app.route('/search',methods=['GET'])
def search():

    if check_auth():
        return check_auth()
    if 'query' not in request.args:
        query = ""
    else: 
        query = request.args.get('query')

    campus = {} #this is beyond inefficient 
    with open("SF_fulldata","rb") as f:
        campus['SF'] = pickle.load(f)
    with open("GB_fulldata","rb") as f:
        campus['GB'] = pickle.load(f)
    with open("BA_fulldata","rb") as f:
        campus['BA'] = pickle.load(f)

    listing = []

    #the dictionaries are not indexed in [day][hour]
    for day in range(7):
        for hour in range(16):
            for building in campus:
                for room in campus[building]:
                    booking = campus[building][room][hour][day]
                    if query.upper() in booking: 
                        listing.append((booking,building,room,hour,day+7))

    return render_template('search.html',results=listing)


@app.route('/',methods=['GET'])
def home_page():

    if check_auth():
        return check_auth()
    
    q_s = request.query_string.decode('utf-8')
    ct = datetime.datetime.now() 
    time = ct.hour  
    day = ct.weekday() 
    b = 'BA'
    if q_s == "GB":
        b = "GB"
    if q_s == "SF":
        b = "SF" 
    if "TEST" in q_s:
        b = request.args.get('building')
        time = int(request.args.get('time'))
        day = int(request.args.get('day'))
        ct = datetime.datetime(ct.year,ct.month,day,hour = time)
     
    ts = ct.strftime("%A, %B, %d %I:%M%p")
    rooms1 = room_plz(b,day,time)
    rooms2 = room_plz(b,day,time+1)

    return render_template('layout.html',b=b,ts=ts,rooms1=rooms1,rooms2=rooms2)

if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)
