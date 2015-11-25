import platform, sys, os, datetime,pickle 
from webob import Response,Request

def room_plz(b,d,t):
    #download_BA()   #only download when you actually need to update the data       
    building = b
    time = t  
    response = [] 


    with open(b+"_organized",'rb') as f:
        availability = pickle.load(f)


    if time>=7 and time <= 22:
        response = availability[d][time-7]
    return response #response is a dictionary whose keys are the room numbers, and values are the duration 

def construct_page(q_s):
    ct = datetime.datetime.now() 
    time = ct.hour  
    day = ct.weekday() 
    building = 'BA'
    if q_s == "GB":
        building = "GB"
    if q_s == "SF":
        building = "SF" 

 
    html_start = """<!DOCTYPE HTML> \n
    <html>"""
    
    head = """<head> 
                <title>Test Server plz ignore</title>
                <meta charset = \"utf-8\" /> 
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <link rel="stylesheet" href="/main.css" />
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
    
    body = """<body> 
                <section id = \"banner\"> 
                    <h2><a href =/M7RYRBm.gif><strong>I can haz room?</strong></a></h2></section>
                <section id = "one" class="wrapper special">
                    <h2><a href =/?BA>BA </a><a href =/?GB>GB </a><a href=/?SF>SF </a></h2>"""
    body +="""<p>You requested a room in """ +building+""" on<br>"""+ct.strftime("%A, %B, %d %I:%M%p") +"""</p>""" 
    body +="""<ul class="actions"> """
                
    rooms = room_plz(building,day,time)
    for key in sorted(rooms):
        body += """<li><a href="#" class="button special"><p>"""+key +""" : """ + str(rooms[key]) +""" hr</p></a></li>\n"""                
    body += """</ul> """
    if len(rooms) == 0:
        body += """<p>Sorry! No rooms are available right now.</p>"""
    
    body += """<p>These rooms are available in the next hour:</p>"""
    body +="""<ul class="actions"> """
                
    rooms = room_plz(building,day,time+1)
    for key in sorted(rooms):
        body += """<li><a href="#" class="button special">"""+key+""" : """+str(rooms[key])+""" hr</a></li>\n"""                
    body += """</ul></section></body>"""
    

    html_end = """</html>"""
    
    return html_start + head + body + html_end 

def application (environ, start_response):
    os.chdir('/var/www/html') 
    req = Request(environ)
    text = construct_page(req.query_string) 
    resp = Response(body=text)
    resp.content_type = 'text/html'
    return resp(environ,start_response) 



if __name__=="__main__":
    print(construct_page("test"))

