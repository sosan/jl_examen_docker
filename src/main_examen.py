# -*- coding: utf -*-
"""

APPLICACION COCHES DONDE CALCULA LOS GASTOS MENSUALES
MUESTRA UN HISTORICO DE LOS MESES TRANSCURRIDOS


"""
import os
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_bootstrap import Bootstrap

# proias
from ModuloLogica.ManagerLogica import ManagerLogica

# instanciaciones e inicializciones
app = Flask(__name__)
app.secret_key = "skjsdkjsdf"
bootstrap = Bootstrap(app)
managerlogica = ManagerLogica()


@app.route("/", methods=["get"])
def home():
    return render_template("index.html")


@app.route("/", methods=["post"])
def recibir_login():
    if "usuario" and "password" in request.form:

        ok = managerlogica.comprobarusuario(request.form["usuario"], request.form["password"])
        if ok == True:
            # existe usuario
            datosusuario = managerlogica.getusuario(request.form["usuario"], request.form["password"])

            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]
            if "nombre" in datosusuario:
                session["nombre"] = datosusuario["nombre"]

            return redirect(url_for("profile"))

    return redirect(url_for("home"))


@app.route("/profile", methods=["get"])
def profile():
    if "usuario" and "password" in session:
        ok = managerlogica.comprobarusuario(session["usuario"], session["password"])
        if ok == True:

            resultados = managerlogica.getgastosmensules(session["usuario"])
            if "calculo_gasto_electricidad_mes" and "calculo_gasto_gasolina_mes" and "gasto_seguro" in session:
                calculo_gasto_electricidad_mes = session.pop("calculo_gasto_electricidad_mes")
                calculo_gasto_gasolina_mes = session.pop("calculo_gasto_gasolina_mes")
                calculo_gasto_seguro_mes = session.pop("calculo_gasto_seguro_mes")
                mes = session.pop("mes")

                return render_template("profile.html", hoy=datetime.utcnow(),
                                       calculo_gasto_electricidad_mes=calculo_gasto_electricidad_mes,
                                       calculo_gasto_gasolina_mes=calculo_gasto_gasolina_mes,
                                       calculo_gasto_seguro_mes=calculo_gasto_seguro_mes,
                                       mes=mes
                                       )

            return render_template("profile.html", hoy=datetime.utcnow(), nombre=session["nombre"],
                                   historico=resultados)

    return render_template("profile.html", hoy=datetime.utcnow())


@app.route("/profile", methods=["post"])
def recibir_datos_gastos():
    if "gasto_electricidad" and "gasto_gasolina" and "gasto_seguro" in request.form:

        try:

            gasto_electricidad = float(request.form["gasto_electricidad"])
            gasto_gasolina = float(request.form["gasto_gasolina"])
            gasto_seguro = float(request.form["gasto_seguro"])
            # gasto_itv = float(request.form["gasto_itv"])

            calculo_gasto_electricidad_mes = gasto_electricidad * 24 * 30
            calculo_gasto_gasolina_mes = gasto_gasolina * 4
            calculo_gasto_seguro_mes = gasto_seguro / 12

            insertado_ok = managerlogica.insertar_datos_calculo(
                session["usuario"],
                request.form["mes"],
                calculo_gasto_electricidad_mes,
                calculo_gasto_gasolina_mes,
                calculo_gasto_seguro_mes
            )

            # session["calculo_gasto_electricidad_mes"] = calculo_gasto_electricidad_mes
            # session["calculo_gasto_gasolina_mes"] = calculo_gasto_gasolina_mes
            # session["calculo_gasto_seguro_mes"] = calculo_gasto_seguro_mes
            # session["mes"] = request.form["mes"]

            return redirect(url_for("profile"))


        except ValueError:
            raise Exception("No posible conversion {0}".format(
                request.form["gasto_electricidad"],
                request.form["gasto_gasolina"],
                request.form["gasto_seguro"]
                # request.form["gasto_itv"]

            ))


@app.route("/registro", methods=["get"])
def registro():
    if "errores" in session:
        errores = session.pop("errores")
        return render_template("registro.html", errores=errores)

    return render_template("registro.html")


@app.route("/registro", methods=["post"])
def recibir_datos_registro():
    if "usuario" and "password" and "nombre" in request.form:
        comprobacion = managerlogica.comprobarusuario(
            request.form["usuario"],
            request.form["password"])

        if comprobacion == True:

            session["usuario"] = request.form["usuario"]
            session["password"] = request.form["password"]
            session["nombre"] = request.form["nombre"]
            return redirect(url_for("profile"))
            # else:
            #     session["errores"] = "No posible registro"
        else:
            registro = managerlogica.registrarusuario(request.form["usuario"], request.form["password"],
                                                      request.form["nombre"])
            if registro == True:
                session["usuario"] = request.form["usuario"]
                session["password"] = request.form["password"]
                session["nombre"] = request.form["nombre"]
                return redirect(url_for("profile"))

    return redirect(url_for("registro"))


if __name__ == "__main__":
    env_port = int(os.environ.get("PORT", 5000))
    env_debug = os.environ.get("FLASK_DEBUG", 1)
    # Dockerfile o run tenemos la opcion de la varaible de entorno FLASK_DEBUG = 1/0
    # docker build .... --build-arg FLASK_ENV="development"
    # docker run ........ -e "FLASK_ENV=production"
    app.run(host="0.0.0.0", port=env_port, debug=env_debug)
