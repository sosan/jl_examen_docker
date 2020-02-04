from datetime import datetime
from datetime import timedelta


from ModuloMongo.ManagerMongo import managermongo
import calendar


class ManagerLogica():
    def __init__(self):
        self.managermongo = managermongo

    def comprobarusuario(self, usuario, password):
        ok = self.managermongo.comprobarusuario(usuario, password)
        return ok

    def getusuario(self, usuario, password):
        datos = self.managermongo.getusuario(usuario, password)
        return datos

    def registrarusuario(self, usuario, password, nombre):
        ok = self.managermongo.registrarusuario(usuario, password, nombre)
        return ok

    def insertar_datos_calculo(self,  usuario, mes,
                calculo_gasto_electricidad_mes,
                calculo_gasto_gasolina_mes,
                calculo_gasto_seguro_mes):
        ok = self.managermongo.insertar_datos_calculo(usuario, mes,
            calculo_gasto_electricidad_mes,
            calculo_gasto_gasolina_mes,
            calculo_gasto_seguro_mes

        )
        return ok

    def getgastosmensules(self, usuario):
        datos = self.managermongo.getgastosmensuales(usuario)
        return datos