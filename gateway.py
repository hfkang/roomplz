import sys,os
sys.path.insert(0, '/app/roomplz')
from hello import app as roomplz
from werkzeug.wsgi import DispatcherMiddleware
sys.path.insert(0, '/app/examreminder')
from exams import exrem


os.chdir('/app/roomplz')

application = DispatcherMiddleware(roomplz, {'/remind':exrem}) 
