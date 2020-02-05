"""
APLICACION PROFESOR


"""

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_bootstrap import Bootstrap

from pymongo import MongoClient
from bson.objectid import ObjectId

from datetime import datetime
from datetime import timedelta
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


import os

app = Flask(__name__)
app.secret_key = "fkskls"
bootstrap = Bootstrap(app)


# conexion con mongodb
MONGO_ATLAS = "mongodb+srv://pepito:pepito@cluster0-6oq5a.gcp.mongodb.net"
cliente = MongoClient(MONGO_ATLAS, ssl_cert_reqs=False)
db = cliente["appcoches"]
cursorcoches = db["coche"]
cursoradmin = db["admin"]
# insert ejemplo
cursoradmin.insert_one({"testing": "testing"})

# --- solo pasa en el test ---

@app.route("/")
def home():
    
    return render_template("index_profe.html")

@app.route("/")
def recibir_datos_gastos():
    
    return render_template("index_profe.html")


if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 5000))
    env_debug = os.environ.get("FLASK_DEBUG", 1)
    # Dockerfile o run tenemos la opcion de la varaible de entorno FLASK_DEBUG = 1/0
    # docker build .... --build-arg FLASK_ENV="development"
    # docker run ........ -e "FLASK_ENV=production"
    app.run(host="0.0.0.0", port=env_port, debug=env_debug)