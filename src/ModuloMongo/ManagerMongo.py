import locale
import uuid

from pymongo import MongoClient
from bson.objectid import ObjectId

from datetime import datetime
from datetime import timedelta
from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


class ManagerMongo:
    def __init__(self):

        self.MONGO_URL = "mongodb+srv://{0}:{1}@{2}"
        self.cliente: MongoClient = None
        self.db: Database = None
        self.coche: Collection = None
        self.cursoradmin: Collection = None

    def conectDB(self, usuario, password, host, db, coleccion):
        try:
            self.cliente = MongoClient(self.MONGO_URL.format(usuario, password, host), ssl_cert_reqs=False)
            self.db = self.cliente[db]
            self.coche = self.db[coleccion]
            self.cursoradmin = self.db["admin"]

        except ConnectionFailure:
            raise Exception("Servidor no disponible")

    def comprobarusuario(self, usuario, password):
        resultado = self.cursoradmin.find_one({"usuario": usuario, "password": password})
        if resultado != None:
            if len(resultado) > 0:
                return True
        return False

    def getusuario(self, usuario, password):
        datos = self.cursoradmin.find_one({"usuario": usuario, "password": password})
        if datos != None:
            if len(datos) > 0:
                return datos
        return None

    def registrarusuario(self, usuario, password, nombre):
        registro = self.cursoradmin.insert_one({"usuario": usuario, "password": password, "nombre": nombre})
        if registro.inserted_id != None:
            return True
        return False

    def insertar_datos_calculo(self, usuario, mes,
                               calculo_gasto_electricidad_mes,
                               calculo_gasto_gasolina_mes,
                               calculo_gasto_seguro_mes):
        # si existe acutalizar

        datos = self.coche.find_one({"usuario": usuario, "mes": mes})
        if datos != None:
            # existe
            c_electricidad_mes = datos["calculo_gasto_electricidad_mes"] + calculo_gasto_electricidad_mes
            c_gasolina_mes = datos["calculo_gasto_gasolina_mes"] + calculo_gasto_gasolina_mes
            c_seguro_mes = datos["calculo_gasto_seguro_mes"] + calculo_gasto_seguro_mes

            actualizado = self.coche.find_one_and_update(
                {"usuario": usuario, "mes": mes},
                {"$set": {
                    "calculo_gasto_electricidad_mes": c_electricidad_mes,
                    "calculo_gasto_gasolina_mes": c_gasolina_mes,
                    "calculo_gasto_seguro_mes": c_seguro_mes

                }}
               )
            return actualizado
        else:
            # si no existe insertarlo
            insertado = self.coche.insert_one(
            {
                "usuario": usuario,
                 "mes": mes,
                "calculo_gasto_electricidad_mes": calculo_gasto_electricidad_mes,
                "calculo_gasto_gasolina_mes": calculo_gasto_gasolina_mes,
                "calculo_gasto_seguro_mes": calculo_gasto_seguro_mes

             })
            if insertado.inserted_id != None:
                return True
            return False

        # insertado = self.coche.update_one({"usuario": usuario},
        #                                   {"$push":
        #                                       {
        #                                           "gastos":
        #                                               [
        #                                                   {
        #                                                       "mes": mes,
        #                                                       "calculo_gasto_electricidad_mes": calculo_gasto_electricidad_mes,
        #                                                       "calculo_gasto_gasolina_mes": calculo_gasto_gasolina_mes,
        #                                                       "calculo_gasto_seguro_mes": calculo_gasto_seguro_mes
        #                                                   }
        # 
        #                                               ]
        # 
        #                                       }
        # 
        #                                   }
        #                                   )


    def getgastosmensuales(self, usuario):
        resultado = list(self.coche.find({"usuario": usuario}))
        return resultado

managermongo = ManagerMongo()
managermongo.conectDB("pepito", "pepito", "cluster0-6oq5a.gcp.mongodb.net",
                    db="jl_examen_docker", coleccion="coche")
#
# managermongo.insertar_datos_calculo(
#     "h@h.com", "enero", 100, 200, 300
# )
# managermongo.insertar_datos_calculo(
#     "h@h.com", "febrero", 100, 200, 300
# )
