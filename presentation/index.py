from business.admin import VerifierGral, Verificacion, ModificarUsuario, AgregarUsuario
import getpass


class App:
    def __init__(self):
        self.usuario = ""
        self.contrasena = ""


    def AppMonedas(self):
        Admi = VerifierGral()
        print("Bienvenido a la app de Monedas!!")
        print("Seleccione una opcion: ")
        login = input("1 - Estoy registrado / 2 - Deseo registrarme: ")
        if (login == "1" or login == "2"):
            if (login == "1"):
                try:
                    self.usuario = input("Por favor ingrese el usuario: ")
                    contrasena = getpass.getpass("Por favor ingrese la contraseña: ")
                    myVerifier = Verificacion(contrasena,self.usuario)
                    if (myVerifier.Verificador()):
                        #aca va self.Menu()#
                        self.Menu()
                    else:
                        print("Los datos ingresados son incorrectos")
                except Exception as e:
                    print(e.args[0])

            elif (login == "2"):
                try:
                    self.usuario = input("Ingrese un nombre de usuario: ")
                    contrasena1 = getpass.getpass("Ingrese una contraseña: ")
                    contrasena2 = getpass.getpass("Ingrese la contraseña nuevamente: ")                            
                    agrego = AgregarUsuario(contrasena1, contrasena2, self.usuario)
                    agrego.agregar()
                    #aca va el self.Menu()#
                    self.Menu()
                except Exception as e:
                    print(e.args[0])
            
        else:
            print("La opcion ingresada es invalida")

    ##### aca desarrollo el menu ####

    def Menu(self):
        Admi = VerifierGral()
        
        while True:
            print("1 - Modificar contraseña ya existente")
            print("2 - Agregar Moneda")
            print("3 - Depositar dinero en cuenta ARS")
            print("4 - Comprar o vender Monedas")
            print("5 - Salir")
            opcion = input("Seleccionar una opcion: ")

            if (opcion == "1"):
                # modificar contrasena ya existente
                try:
                    self.usuario = input("Ingrese el usuario que desea modificar: ")
                    contrasena1 = getpass.getpass("Ingrese la nueva contraseña: ")
                    contrasena2 = getpass.getpass("Ingrese nuevamente la contraseña: ")
                                            
                    Modifico = ModificarUsuario(contrasena1, contrasena2, self.usuario)
                    Modifico.modificar()
                except Exception as e:
                    print(e.args[0])  

            elif (opcion == "2"):
                # agregar moneda
                try:                                                                 
                    curr_code = input("Ingrese el codigo de moneda deseado: ")   
                    Admi.createAccount(curr_code,self.usuario)
                except Exception as e:
                    print(e.args[0])
                
            elif (opcion == "3"):                                           
                # depositar dinero en cuenta ARS
                try:
                    curr_code = "ARS"
                    monto = input("Ingrese el monto que desea: ")
                    Admi.depositarPesos(self.usuario,curr_code,monto)
                except Exception as e:
                    print(e.args[0])

            elif (opcion == "4"):
                operacion = input("1 - Comprar / 2 - Vender: ")

                if (operacion == "1"):
                    # aca hago la compra de moneda
                    try:                                       
                        curr_code = input("Que moneda desea comprar: ")
                        monto = input("Monto que desea comprar: ")       
                        Admi.compraMoneda(self.usuario,monto,curr_code)
                    except Exception as e:
                        print(e.args[0])
                    
                elif (operacion == "2"):
                    # aca hago operacion de venta
                    try:
                        curr_code = input("Que moneda desea vender para obtener pesos: ")   
                        monto = input("Monto que desea vender: ")    
                        Admi.ventaMoneda(self.usuario,monto,curr_code)
                    except Exception as e:
                        print(e.args[0])
                    
                else:
                    print("Opcion ingresada es invalida")

            elif (opcion == "5"):
                # aca salgo del programa
                break
            else:
                print("Opcion ingresada es invalida")