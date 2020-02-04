# -*- coding: utf -*-
"""

APPLICACION 
NOMBRE

"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session


# instanciaciones e inicializciones
app = Flask(__name__)
app.secret_key = "skjsdkjsdf"


@app.route("/", methods=["get"])
def home():
    return render_template("index.html")



@app.route("/", methods=["post"])
def recibir_login():
    
    if "usuario" and "password" in request.form:
        
        ok = managerlogica.comprobarusuario(request.form["usuario"], request.formp["password"])
        
        
        
        return redirect(url_for(""))    
    return redirect(url_for("home"))


if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 5000))
    env_debug = os.environ.get("FLASK_DEBUG", 1)
    # Dockerfile o run tenemos la opcion de la varaible de entorno FLASK_DEBUG = 1/0
    # docker build .... --build-arg FLASK_ENV="development"
    # docker run ........ -e "FLASK_ENV=production"
    app.run(host="0.0.0.0", port=env_port, debug=env_debug)


