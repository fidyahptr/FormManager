from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# from interfaces.web.routes.text2sqlBP import t2s
from interfaces.web.routes.indexBP import indexBP

# app.register_blueprint(t2s, url_prefix='/chat')
app.register_blueprint(indexBP, url_prefix='/')

@app.route("/")
def index():

    return 'halo'

