from currencies import curr
import requests as rq
import bcrypt
from decimal import Decimal
import sqlobject as SO

#Creacion de tablas y su conexion
database = 'mysql://root:root@localhost/appcotizacion'
__connection__ = SO.connectionForURI(database)

class Usuario(SO.SQLObject):

    usuario = SO.StringCol(length = 40, varchar = True, unique = True)
    contra = SO.StringCol(length = 80, varchar = True)
    cuentas = SO.MultipleJoin('Cuentas')
Usuario._connection = __connection__
# Usuario.dropTable(ifExists = True)
# Usuario.createTable()

class Currency(SO.SQLObject):
    
    currencyCode = SO.StringCol(length = 3, varchar = True)
    cuentas = SO.MultipleJoin('Cuentas')
Currency._connection = __connection__
# Currency.dropTable(ifExists = True)
# Currency.createTable()

# codigos = curr.keys()
# for codigo in codigos:
#      Currency(currencyCode = codigo)

class Cuentas(SO.SQLObject):

    currency = SO.ForeignKey('Currency', default="None", cascade=True)
    usuario = SO.ForeignKey('Usuario', default="None", cascade=True, dbName='usuario')
    cantidad = SO.DecimalCol(size=8, precision=2, default="0.00")
    
Cuentas._connection = __connection__
# Cuentas.dropTable(ifExists = True)
# Cuentas.createTable()

##################################### empieza el data #########################

#aca agrego, modifico y verifico

class Administrador:
    def UsuarioContrasena(self, contrasena, usuario):
        usuBusqueda = Usuario.selectBy(usuario=usuario).getOne()
        contra_hash = usuBusqueda.contra.encode('utf-8')

        if usuBusqueda.usuario == usuario and bcrypt.checkpw(contrasena.encode('utf-8'), contra_hash):
            return contrasena, usuario
        else:
            return None, None

    def modificarUsuario(self,contrasena1,contrasena2,usuario):
            usuBusqueda = Usuario.selectBy(usuario=usuario).getOne()
            try:
                contra_hash = bcrypt.hashpw(contrasena1.encode("utf-8"), bcrypt.gensalt())
                nueva_contrasena = contra_hash.decode("utf-8")

                if(usuario == usuBusqueda.usuario):
                    if(contrasena1 == contrasena2):
                        usuBusqueda.contra = nueva_contrasena
                return True       
            except SO.SQLObjectNotFound:
                return False
            

    def agregarUsuario(self,contrasena1,contrasena2,usuario):
        if contrasena1 == contrasena2:
            contra_hash = bcrypt.hashpw(contrasena1.encode("utf-8"), bcrypt.gensalt())
            contra_hash_str = contra_hash.decode("utf-8")
            nuevo_usuario = Usuario(usuario=usuario, contra=contra_hash_str)
            nuevo_usuario.sync() 
            usuario_id = nuevo_usuario.id
            Cuentas(currency=7, usuario=usuario_id, cantidad="0.00")
            return True
        else:
            return False

class data_helper:

    def isCurrCodeValid(self,curr_code):
        if curr_code in curr.keys():
            return True
        return False

    def AccountExist(self,curr_code,usuario):
        
        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        usuario_obj = Usuario.selectBy(usuario=usuario).getOne()
        nuevaCuenta = Cuentas.selectBy(currency=currency_obj, usuario=usuario_obj).count()
        return nuevaCuenta > 0

    def createAccount(self,curr_code,usuario):

        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        usuario_obj = Usuario.selectBy(usuario=usuario).getOne()
        Cuentas(currency=currency_obj, usuario=usuario_obj)

    def obtenerSaldo(self, curr_code, usuario):
        currency_obj = self.objectoMoneda(curr_code)
        usuario_obj = self.objectoUsuario(usuario)

        cuenta_obj_peso = Cuentas.selectBy(currency=currency_obj, usuario=usuario_obj).getOne()
        saldo = cuenta_obj_peso.cantidad
        return saldo


    def depositoMoneda(self, usuario, curr_code, monto):

        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        usuario_obj = Usuario.selectBy(usuario=usuario).getOne()
        cuenta_obj = Cuentas.selectBy(currency=currency_obj, usuario=usuario_obj).getOne()
        cuenta_obj.cantidad += Decimal(monto)
        cuenta_obj.sync()

    def obtenerUsuario(self,usuario):
        usuario_obj = Usuario.selectBy(usuario=usuario).getOne()
        usuario_id = usuario_obj.id
        return usuario_id

    def objectoMoneda(self,curr_code):
        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        return currency_obj

    def objectoUsuario(self,usuario):
        usuario_obj = Usuario.selectBy(usuario=usuario).getOne()
        return usuario_obj

    
    def restoMonto(self, saldo, monto, curr_code, usuario):
        usuario_obj = self.obtenerUsuario(usuario)
        currency_obj = self.objectoMoneda(curr_code)
        monto = Decimal(saldo) - Decimal(monto)
        resultado = Cuentas.select(SO.AND((Cuentas.q.currency == currency_obj), (Cuentas.q.usuario == usuario_obj)))
        cuenta = resultado[0]
        cuenta.cantidad = monto
        return cuenta

    def sumoMonto(self, saldo, monto, curr_code, usuario):
        usuario_obj = self.obtenerUsuario(usuario)
        currency_obj = self.objectoMoneda(curr_code)

        monto = Decimal(saldo) + Decimal(monto)
        resultado = Cuentas.select(SO.AND((Cuentas.q.currency == currency_obj), (Cuentas.q.usuario == usuario_obj)))
        cuenta = resultado[0]
        cuenta.cantidad = monto 
        return cuenta
    
    def conexionFixe(self,curr_code):
        url = f"http://data.fixer.io/api/latest?access_key=27bc953cfda45f1f9fa6131efa757947&symbols=ARS,{curr_code}"
        response = rq.get(url)
        res_json = response.json()
        return res_json

    def cotizacion(self,datos,curr_code):
        return Decimal(datos['rates'][curr_code])


