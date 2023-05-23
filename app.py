from flask import *

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')

