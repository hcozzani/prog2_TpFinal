from currencies import curr
from os import path
import json
import requests as rq
import bcrypt
from decimal import Decimal
import os


class Administrador:
    def __init__(self):
        self.filepath="usuarios.json" 
        
    def UsuarioContrasena(self,contrasena,usuario):
        with open(self.filepath, "r") as f:
            serObj = f.read()
            data = json.loads(serObj)
            for dato in data:
                contra = dato["contrasena"]
                usu = dato["usuario"]
                if bcrypt.checkpw(contrasena.encode("utf-8"), contra.encode("utf-8")):
                    if usuario == usu:
                        return contrasena, usuario
        return None, None

    def agregarUsuario(self,contrasena1,contrasena2,usuario):
        if contrasena1 == contrasena2:
                with open(self.filepath, 'r') as f:  
                    serObj = f.read()
                    data = json.loads(serObj)
                nombreJson= set(usuario["usuario"] for usuario in data)
                if usuario in nombreJson:
                    raise Exception("El usuario ya existe")
                     
                contra_hash = bcrypt.hashpw(contrasena1.encode("utf-8"), bcrypt.gensalt())
                data.append({"contrasena": contra_hash.decode("utf-8"), "usuario": usuario})

                with open(self.filepath, 'w') as f:
                    json.dump(data, f, indent=4)

                usu = f"{usuario}.json"

                datosCuenta = {
                    "ARS":"0.00"
                }

                with open(usu, 'w') as f:
                    json.dump(datosCuenta, f, indent=4)

                return True
        else:
                return False

    def modificarUsuario(self,contrasena1,contrasena2,usuario):
        with open(self.filepath, 'r') as f:
            serObj = f.read()
            data = json.loads(serObj)

        ok = False
        for item in data:
            contra = item["contrasena"]
            usu = item["usuario"]
            if contrasena1 == contrasena2:
                if usu == usuario:
                    contra_hash = bcrypt.hashpw(contrasena1.encode("utf-8"), bcrypt.gensalt())
                    item["contrasena"] = contra_hash.decode("utf-8")
                    ok = True
        if ok:
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
                return True
        return False



class data_helper:

    def checkAccounts(self,usuario):
        filename = usuario + ".json"
        if path.exists(filename):
            if self.AccountExist("ARS",usuario)==True:
                return True
            else:
                return False
        with open(filename,"w") as f:
            account_des = {"ARS":"0.00"}
            account_ser = json.dumps(account_des,indent=4)
            f.write(account_ser)
            return True

    def isCurrCodeValid(self,curr_code):
        if curr_code in curr.keys():
            return True
        return False

    def AccountExist(self,curr_code,usuario):
        filename = usuario + ".json"
        with open(filename,"r") as f:
            file_content = f.read()
            file_des=json.loads(file_content)
            if curr_code in file_des.keys():
                return True
            else:
                return False

    def createAccount(self,curr_code,usuario):
        filename = usuario + ".json"
        accounts_des = {}
        with open(filename,"r") as f:
            file_content = f.read()
            accounts_des=json.loads(file_content)
        accounts_des.update({curr_code:"0.00"})
        with open(filename,"w") as f:
            accounts_ser = json.dumps(accounts_des,indent=4)
            f.write(accounts_ser)

    def getJson(self,usuario):
        archivo = usuario + ".json"
        return archivo

    def obtenerUsuario(self, usuario):
        archivo = usuario + ".json"
        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                datos_usuario = json.load(f)
            return datos_usuario.get("usuario")

    def obtenerSaldo(self,curr_code,usuario):
        archivo = self.getJson(usuario)
        with open(archivo, "r") as f:
            cuenta = json.load(f)
        saldo_X = Decimal(cuenta[curr_code])
        return saldo_X

    def depositoMoneda(self,usuario,curr_code,monto):
        archivo = self.getJson(usuario)

        with open(archivo, "r") as f:
            usuario = json.load(f)

        montoDecimal = Decimal(str(monto))
        usuario[curr_code] = str(Decimal(usuario[curr_code]) + montoDecimal)
        
        with open(archivo, "w") as f:
            json.dump(usuario, f, indent=4)

    def obtenerSaldo(self,curr_code,usuario):
        archivo = self.getJson(usuario)
        with open(archivo, "r") as f:
            cuenta = json.load(f)
        saldo_X = Decimal(cuenta[curr_code])
        return saldo_X

    def restoMonto(self, saldo, monto, curr_code, usuario):
        saldo = self.obtenerSaldo(curr_code, usuario)        
        archivo = usuario + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        saldoTotal = Decimal(saldo) - Decimal(monto)
        cuentas[curr_code] = "{:.2f}".format(saldoTotal) 

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)

    def sumoMonto(self, saldo, monto, curr_code, usuario):
        saldo = self.obtenerSaldo(curr_code, usuario)        
        archivo = usuario + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        saldoTotal = Decimal(saldo) + Decimal(monto)
        cuentas[curr_code] = "{:.2f}".format(saldoTotal)

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)


    def conexionFixe(self,curr_code):
        
        url = f"http://data.fixer.io/api/latest?access_key=27bc953cfda45f1f9fa6131efa757947&symbols=ARS,{curr_code}"
        response = rq.get(url)
        res_json = response.json()
        return res_json

    def cotizacion(self,datos,curr_code):
        return Decimal(datos['rates'][curr_code])

