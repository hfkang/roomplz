import platform, sys, os, datetime,pickle 
from webob import Response,Request

#Pulls the room data from the archived dictionary
def room_plz(b,d,t):
    building = b
    time = t  
    response = [] 


    with open(b+"_organized",'rb') as f:
        availability = pickle.load(f)


    if time>=7 and time <= 22:
        response = availability[d][time-7]
    return response #response is a dictionary whose keys are the room numbers, and values are the duration 

#Generates the html response
def construct_page(q_s):
    ct = datetime.datetime.now() 
    time = ct.hour  
    day = ct.weekday() 
    building = 'BA'
    if q_s == "GB":
        building = "GB"
    if q_s == "SF":
        building = "SF" 
    if q_s == "TEST":
        building = "BA"
        day = 1
        time = 12
 
    html_start = """<!DOCTYPE HTML> \n
    <html>"""
    
    head = """<head> 
                <title>EngSci dkm pls</title>
                <meta charset = \"utf-8\" /> 
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <link rel="stylesheet" href="main.css" />
                <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
                <link rel="apple-touch-icon" sizes="60x60" href="/apple-touch-icon-60x60.png">
                <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
                <link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
                <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
                <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
                <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">
                <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
                <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
                <link rel="icon" type="image/png" href="/favicon-194x194.png" sizes="194x194">
                <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
                <link rel="icon" type="image/png" href="/android-chrome-192x192.png" sizes="192x192">
                <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
                <link rel="manifest" href="/manifest.json">
                <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5">
                <meta name="msapplication-TileColor" content="#da532c">
                <meta name="msapplication-TileImage" content="/mstile-144x144.png">
                <meta name="theme-color" content="#ffffff"> 
                <script>
                  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

                  ga('create', 'UA-70666671-1', 'auto');
                  ga('send', 'pageview');

                </script>
                            </head>"""
    
    body = """<body> 
                <section id = \"banner\"> 
                    <h2><a href =http://thecatapi.com/api/images/get?format=src><strong>I can haz room?</strong></a></h2></section>
                <section id = "one" class="wrapper special">
                    <a href="?BA" class="button alt big">BA</a>
                    <a href="?GB" class="button alt big">GB</a>
                    <a href="?SF" class="button alt big">SF</a>"""
    body +="""<div class = "inner"><p>These rooms are free in """ +building+""" on<br>"""+ct.strftime("%A, %B, %d %I:%M%p") +"""</p>""" 
    


    body +="""<ul class="actions"> """
                
    rooms = room_plz(building,day,time)
    for key in sorted(rooms):
        body += """<li><a href="#" class="button disabled fit"><p>"""+key +""" : """ + str(rooms[key]) +""" hr</p></a></li>\n"""                
    body += """</ul> """
    if len(rooms) == 0:
        body += """<p>Sorry! No rooms are available right now.</p>"""
    
    body += """<p>These rooms are available in the next hour:</p>"""
    body +="""<ul class="actions"> """
                
    rooms = room_plz(building,day,time+1)
    for key in sorted(rooms):
        body += """<li><a href="#" class="button disabled fit">"""+key+""" : """+str(rooms[key])+""" hr</a></li>\n"""                
    body += """</ul></div></section></body>"""
    

    html_end = """</html>"""
    
    return html_start + head + body + html_end 

def login():
    html_start = """<!DOCTYPE HTML> \n
    <html>"""
    
    head = """<head> 
                <title>Login</title>
                <meta charset = \"utf-8\" /> 
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <link rel="stylesheet" href="main.css" />
                <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
                <link rel="apple-touch-icon" sizes="60x60" href="/apple-touch-icon-60x60.png">
                <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
                <link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
                <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
                <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
                <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">
                <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
                <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
                <link rel="icon" type="image/png" href="/favicon-194x194.png" sizes="194x194">
                <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
                <link rel="icon" type="image/png" href="/android-chrome-192x192.png" sizes="192x192">
                <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
                <link rel="manifest" href="/manifest.json">
                <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5">
                <meta name="msapplication-TileColor" content="#da532c">
                <meta name="msapplication-TileImage" content="/mstile-144x144.png">
                <meta name="theme-color" content="#ffffff"> 
                <script>
                  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

                  ga('create', 'UA-70666671-1', 'auto');
                  ga('send', 'pageview');

                </script>
                            </head>"""
    
    body = """<body style='background-color:#f7f7f7'><section id='three' class='wrapper style2 special'>
        <div class ='inner narrow'>
            <h2>Please login:</h2>

            <form class = 'grid-form' action='/' method = 'post'>
            <div class = 'form-control'>
            <input type='password' name='pswd'>
            </div>
            <div class = 'form-control'>
            <input type='submit' value='Submit'>
            </div> 
            </form>

        </div> 

            </section></style></body>"""


    html_end = """</html>"""

    return html_start + head + body + html_end   

def francis():
     html_start = """<!DOCTYPE HTML> \n
    <html>"""
    
    head = """<head> 
                <title>Francis Kang</title>
                <meta charset = \"utf-8\" /> 
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <link rel="stylesheet" href="main.css" />
                <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
                <link rel="apple-touch-icon" sizes="60x60" href="/apple-touch-icon-60x60.png">
                <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
                <link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
                <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
                <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
                <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">
                <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
                <link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
                <link rel="icon" type="image/png" href="/favicon-194x194.png" sizes="194x194">
                <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
                <link rel="icon" type="image/png" href="/android-chrome-192x192.png" sizes="192x192">
                <link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16">
                <link rel="manifest" href="/manifest.json">
                <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5">
                <meta name="msapplication-TileColor" content="#da532c">
                <meta name="msapplication-TileImage" content="/mstile-144x144.png">
                <meta name="theme-color" content="#ffffff"> 
                            </head>"""
    
    body = """<body style='background-color:#f7f7f7'><section id='three' class='wrapper style2 special'>
            <h1>Hi there, I'm Francis Kang.</h2>
            <h2>Education:</h2>
            <p>Engineering Science, University of Toronto</p>
            

            </section></body>"""


    html_end = """</html>"""

    return html_start + head + body + html_end   

   

def application (environ, start_response):
    os.chdir('/var/www/html') 
    req = Request(environ)
    resp = Response()
    cookies = req.cookies
    if req.path == 'francis':
        text = francis()
    else:
        if 'auth' in cookies and cookies['auth'] == 'potato horse banana orange sloth':
            text = construct_page(req.query_string)
        else: 
            #Authentication in progress
            if 'pswd' in req.POST and req.POST['pswd'] == 'potato salad':
                resp.set_cookie("auth",value="potato horse banana orange sloth",domain='toastedsesa.me',overwrite=True,httponly=True,max_age=20000000)
                text = construct_page(req.query_string) 
            else:
                text = login()
    resp.text = text
    resp.content_type = 'text/html'
    return resp(environ,start_response) 



if __name__=="__main__":
    print(construct_page("test"))

