from data.data_helperOrm import Administrador, data_helper
#from data.data_helper import Administrador, data_helper

from decimal import Decimal
import decimal
from decimal import getcontext
import sqlobject as SO


#todo esta parte es del login

class Verificacion:
    
    def __init__(self,contrasena,usuario):
        self.contrasena = contrasena.strip()
        self.usuario = usuario.lower().strip()
        self.data_helper = Administrador()

        
    def Verificador(self):
            try:
                contra, usu = self.data_helper.UsuarioContrasena(self.contrasena, self.usuario)
                if(contra == self.contrasena and usu == self.usuario):
                    return True
                else:
                    raise Exception("Los datos son incorrectos")
            except Exception as ex:
                    raise Exception("Los datos son incorrectos")

class AgregarUsuario:
    
    def __init__(self,contrasena1,contrasena2,usuario):
        self.contrasena1 = contrasena1.strip()
        self.contrasena2 = contrasena2.strip()
        self.usuario = usuario.lower().strip()
        self.data_helper = Administrador()
        
    def agregar(self):
        agreUsu = self.data_helper.agregarUsuario(self.contrasena1, self.contrasena2, self.usuario)
        if(agreUsu):
            return True
        else:
            raise Exception("Las contraseñas no coinciden, intentelo nuevamente!!")
            
class ModificarUsuario:
    def __init__(self,contrasena1,contrasena2,usuario):
        self.contrasena1 = contrasena1.strip()
        self.contrasena2 = contrasena2.strip()
        self.usuario = usuario.lower().strip()
        self.data_helper = Administrador()
    
    def modificar(self):

        modiUsu = self.data_helper.modificarUsuario(self.contrasena1, self.contrasena2, self.usuario)
        if(modiUsu):
            raise Exception("El usuario se ha modificado con exito")
        else:
            raise Exception("Error al modificar el usuario")
        

class VerifierGral:
    usuario = ""
    logueado = False

    def __init__(self):
        self.logueado = True
        self.data_helper = data_helper()
        
    def createAccount(self,curr_code,usuario):

        curr_code=curr_code.lstrip().rstrip().upper()
        if self.data_helper.isCurrCodeValid(curr_code) == False:
            raise Exception("Codigo de moneda no valido")
        if self.data_helper.AccountExist(curr_code,usuario) == True:
            raise Exception("Ya Existe la cuenta que desea crear")
        self.data_helper.createAccount(curr_code,usuario)
        raise Exception("Se creo la cuenta")


    def depositarPesos(self,usuario,curr_code,monto):
        curr_code = curr_code.strip().upper()

        try:
            monto = Decimal(monto)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")
   
        if (monto <= 0):
            raise Exception("Ingrese un monto valido")
        if not self.data_helper.isCurrCodeValid(curr_code):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(curr_code,usuario):
            raise Exception("No tiene cuenta con esa moneda")

        
        self.data_helper.depositoMoneda(usuario,curr_code,monto)
        raise Exception("Dinero acreditado con exito")

    def compraMoneda(self, usuario,monto, curr_code): 
        curr_code = curr_code.strip().upper()
        getcontext().prec = 8
        
        try:
            monto = Decimal(monto)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")

        self.validoMoneda(curr_code,usuario,monto)

        conexion = self.data_helper.conexionFixe(curr_code)      
        cot_Moneda_X = self.data_helper.cotizacion(conexion,curr_code)
        cot_Moneda_Peso = self.data_helper.cotizacion(conexion,"ARS")
        cot_peso_x = cot_Moneda_Peso/cot_Moneda_X

        saldo_peso = self.data_helper.obtenerSaldo("ARS",usuario)
   
        saldo = self.data_helper.obtenerSaldo(curr_code,usuario)

        cantidad_A_Comprar = Decimal(cot_peso_x).quantize(Decimal('0.00')) * Decimal(monto).quantize(Decimal('0.00'))
        
        if cantidad_A_Comprar > saldo_peso:
            raise Exception("No tiene suficiente saldo para realizar la compra")

        self.data_helper.restoMonto(saldo_peso,Decimal(cantidad_A_Comprar),"ARS",usuario)
        self.data_helper.sumoMonto(saldo,Decimal(monto),curr_code,usuario)

        raise Exception("Operacion se realizo con exito")

    def validoMoneda(self,curr_code,cuenta,cantidad):
        if not self.data_helper.isCurrCodeValid(curr_code):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(curr_code,cuenta):
            raise Exception("No tiene una cuenta abierta en esa moneda")
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        if (curr_code == "ARS"):
            raise Exception("No puede comprar pesos argentinos con la misma moneda")

    def ventaMoneda(self, usuario,monto, curr_code):
        curr_code = curr_code.strip().upper()
        getcontext().prec = 8
    
        try:
            monto = Decimal(monto)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")

        self.validoMoneda(curr_code,usuario,monto)
        conexion = self.data_helper.conexionFixe(curr_code)      
        cot_Moneda_X = self.data_helper.cotizacion(conexion,curr_code)
        cot_Moneda_Peso = self.data_helper.cotizacion(conexion,"ARS")
        cot_peso_x = cot_Moneda_Peso/cot_Moneda_X

        saldo = self.data_helper.obtenerSaldo(curr_code,usuario)

        saldo_peso = self.data_helper.obtenerSaldo("ARS",usuario)
        cantidad_A_Comprar = Decimal(cot_peso_x).quantize(Decimal('0.00')) * Decimal(monto).quantize(Decimal('0.00'))
        
        if monto > saldo:
            raise Exception("No tiene suficiente moneda para comprar")

        self.data_helper.restoMonto(saldo,Decimal(monto),curr_code,usuario)
        self.data_helper.sumoMonto(saldo_peso,Decimal(cantidad_A_Comprar),"ARS",usuario)
        raise Exception("Operacion realizada con exito")


