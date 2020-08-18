from Vista import Ventana
from Modelo import Modelo
from Armador import ArmadorModelo
from tkinter import messagebox as MessageBox

class Controlador():
    """
        Clase Controlador del MVC         
    """
    def __init__(self,vista,modelo):
        self.app = vista # Vista de MVC
        self.modelo = modelo # Modelo de MVC
        self.app.boton.configure(command=self.generar_tabla) #Configuracion de evento de boton
        self.app.btn_restricciones.configure(command=self.getMatrizRestricciones) #Configuracion de evento de boton
        self.app.btn_lado_der.configure(command=self.getLadoDerecho) #Configuracion de evento de boton
        self.app.btnCalcular.configure(command=self.armar_modelo) #Configuracion de evento de boton
        
        self.app.ventana.mainloop()


    def generar_tabla(self):
        """
            Genera la tabla con n variables y
            m restricciones a partir de un
            evento de boton
        """
        self.app.crearTabla()
        self.app.mostrar_botones()
    

    def getMatrizRestricciones(self):
        """
            Muestra los elementos ingresados en el
            lado izquierdo de las restricciones
            a partir de evento de boton
        """
        data = self.app.get_matriz_restriccion()   
        MessageBox.showinfo("Datos Restriccion", data)

    def getLadoDerecho(self):
        """
            Muestra los elementos ingresados en el
            lado derecho de las restricciones            
            a partir de evento de boton
        """
        MessageBox.showinfo("Datos Lado derecho", self.app.get_lado_derecho())
        #MessageBox.showinfo("Tipo Opt", self.app.get_signos_restriccion())


    def armar_modelo(self):
        #Permite construir el modelo de programacion entera binaria 
        c = []
        a = []
        b = []
        s = []
        if self.app.validar_fo(): # Valida la entrada de la funcion objetivo
            c = self.app.get_funcion_obj() # Guarda la funcion objetivo
        else: # Si falla muestra el error correspondiente
            self.app.mostrar_mensaje_error("Por favor, ingrese valores válidos en la función objetivo")
        
        if self.app.validar_restriccion(): # Valida la entrada de las restricciones en el lado izquierdo
            a = self.app.get_matriz_restriccion()
            s = self.app.get_signos_restriccion()
        else: # Si falla muestra el error correspondiente
            self.app.mostrar_mensaje_error("Por favor, ingrese valores válidos en la matriz de restricciones")

        if self.app.validar_lado_derecho(): # Valida la entrada de las restricciones en el lado derecho
            b = self.app.get_lado_derecho()
        else: # Si falla muestra el error correspondiente
            self.app.mostrar_mensaje_error("Por favor, ingrese valores válidos en el lado derecho de las restricciones")
        
        if self.app.validar_fo() and self.app.validar_restriccion() and self.app.validar_lado_derecho(): # Validando que todas las entradas sean válidas
            a = ArmadorModelo(self.app.get_num_variables(),self.app.get_tipo_optimizacion(),c,a,s,b) #Crea el objeto para armar un ModeloPL a partir de las entradas
            m = a.generar_modelo()

            self.modelo = Modelo(m) #Pasa el modeloPL a un objeto de la clase Modelo (arbol)
            self.modelo.generar_solucion() # Genera la solucion del problema de programacion binaria
            mod,padre,id_mod,msg,z,x,descrip = self.modelo.get_datos_modelos() # Retorna los datos del arbol de solucion
            self.app.crear_diagrama(mod,padre,id_mod,msg,z,x,descrip,self.modelo.get_x_best(),self.modelo.get_z_best()) # Pasa los datos del árbol al graficador de árboles
    

