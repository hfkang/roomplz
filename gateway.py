import sys,os
sys.path.insert(0, '/home/francis/roomplz')
from hello import app as roomplz
from francis import app as wsgi_francis
sys.path.insert(0, '/home/francis/two')
from main import app as wsgi_startup2
from werkzeug.wsgi import DispatcherMiddleware
sys.path.insert(0, '/home/francis/projincl')
from api import app as wsgi_incl



os.chdir('/home/francis/roomplz')

application = DispatcherMiddleware(roomplz, {'/francis': wsgi_francis,'/startup2': wsgi_startup2, '/projincl': wsgi_incl}) 


"""
def application(environ,start_response):
    os.chdir('/home/francis/roomplz')


    if script == '/francis':    
        return wsgi_francis(environ,start_response)
    elif script == '/startup2':
        os.chdir('/home/francis/two')
        return wsgi_startup2(environ,start_response)
    else:
        return roomplz(environ,start_response)

"""

    
