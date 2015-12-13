import sys,os
sys.path.insert(0, '/home/francis/roomplz')
from hello import app as roomplz
from francis import app as wsgi_francis
 

def application(environ,start_response):
    os.chdir('/home/francis/roomplz')

    script = environ['SCRIPT_NAME']  

    if script == '/francis':    
        return wsgi_francis(environ,start_response)
    else:
        return roomplz(environ,start_response)



