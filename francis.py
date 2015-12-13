from flask import Flask
app = Flask(__name__)


@app.route('/francis')
def francis():
    return "Hi i'm francis"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path




if __name__ == '__main__':
    app.debug = True
    app.run()


