from flask import Flask,render_template
app = Flask(__name__)




@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('francis.html')




if __name__ == '__main__':
    app.debug = True
    app.run()


