from scipy.optimize import linprog
import numpy as np
from Restriccion import Restriccion
from FuncionObjetivo import FuncionObjetivo
class ModeloPL:
    """
    Clase que representa el modelo de programación lineal
    Es un nodo en la estructura árbol de la clase Modelo
    """
    def __init__(self, num_variables,tipo_opt=1,prof = 0,descripcion = ""):
        self.num_variables = num_variables # Numero de variables
        self.num_restricciones = 0 # Numero de restricciones
        self.tipo_optimizacion = tipo_opt # Representa si el modelo minimiza o maximiza
        self.fo = [] # Función objetivo
        self.lista_restricciones = [] # Restricciones 
        self.profundidad = prof # Entero que permite conocer en cual variable se está ramificando en el modelo 
        self.descripcion = descripcion # Descripcion para denotar si se agregan restricciones al modelo

        self.z = 0 # Valor de Z del modelo
        self.x = [] # Valor de las variables del modelo
        self.estado = "" # Sirve para indicar el estado de la optimizacion. Correcta, no acotada, infactible
        self.codigo = 0 # Sirve como bandera para saber si fue optimizado correctamente
        self.padre = 0 # Identificador del subproblema padre
        self.id = 0 # Identificador del subproblema


    def agregar_func_obj(self,fo):
        """
        Permite agregar un objeto de tipo FuncionObjetivo
        al modelo de programación lineal
        """
        self.fo = fo
    

    def agregar_restriccion(self,restriccion):
        """
        Permite agregar un objeto de tipo Restriccion
        al modelo de programación lineal
        """
        self.lista_restricciones.append(restriccion)
        self.num_restricciones = self.num_restricciones + 1


    def crear_fo(self):
        # Crea la funcion objetivo 
        # Para utilizar la libreria linprog de scipy
        c = [self.tipo_optimizacion*i for i in self.fo.get_funcion_objetivo()]
        return c

    #sdsds
    def crear_restricciones(self):
        """ 
            Crea las restricciones en forma de igualdades y desigualdades
            Para utilizar la libreria linprog de scipy
        """
        a_ub = []
        b_ub = []
        a_eq = []
        b_eq = []
        for i in self.lista_restricciones: 
            if i.get_tipo() != 0: # Crea las restricciones de tipo desigualdad
                temp_a = [i.get_tipo()*elem for elem in i.get_lado_izquierdo()] # Multiplica por 1 o -1 de acuerdo si es <= o >=
                temp_b = i.get_tipo()*i.get_valor() # Multiplica por 1 o -1 de acuerdo si es <= o >=
                a_ub.append(temp_a) # Agrega la restricción 
                b_ub.append(temp_b) # Agrega el lado derecho
            else: # Crea las restricciones de tipo igualdad
                temp_a = [elem for elem in i.get_lado_izquierdo()] # Crea el vector que representa lado izquierdo de la igualdad
                temp_b = i.get_valor() # Crea el valor del lado derecho de la restriccion
                a_eq.append(temp_a) # Agrega la restricción 
                b_eq.append(temp_b) # Agrega el lado derecho
            
        return a_ub,b_ub,a_eq,b_eq


    def get_tipo_optimizacion(self):
        """
        Retorna el tipo de optimización
        1 si es Minimizar o -1 si es Maximizar
        """
        return self.tipo_optimizacion

    def get_numero_variables(self):
        """Retorna el número de variables del modelo de programación lineal"""
        return self.num_variables
    def get_numero_restricciones(self):
        """Retorna el número de restricciones del modelo de programación lineal"""
        return self.num_restricciones


    def resolver(self):
        """
            Resuelve el modelo de programación lineal
            del cual se obtiene el valor de Z, las
            variables xi y un mensaje para determinar
            si se realizó correctamente
        """
        c = self.crear_fo() # Crea la Funcion objetivo para optimizar con la libreria linprog de scipy
        a_ub,b_ub,a_eq,b_eq  = self.crear_restricciones() # Crea las restricciones para optimizar con la libreria linprog de scipy

        if len(a_eq) <= 0: # Si no hay restricciones de igualdad, se pasan como parametros nulos al objeto linprog de scipy
            a_eq = None
            b_eq = None

        to = self.get_tipo_optimizacion() # Obtiene min|max (1 o -1)

        #Se crea el objeto linprog para resolver el problema        
        res = linprog(c,a_ub,b_ub,a_eq,b_eq,bounds=(0,1)) # brinda el estado o mensaje del subproblema
        sol = linprog(c,a_ub,b_ub,a_eq,b_eq,bounds=(0,1),method='simplex') #Resuelve el problema mediante simplex
        
        #Determinamos el tipo de solucion
        if res.message.find("infeasible") != -1: #Si el problema es infactible
            self.estado = "Infactible"
            self.codigo = 1
        elif res.message.find("unbounded") != -1: #Si el problema es no acotado
            self.estado = "No Acotado"
            self.codigo = 1
        else: #Si el problema es factible            
            self.z = to*sol.fun # Ajusta el valor de Z si es minimizar o maximizar. Linprog trabaja por defecto con min
            self.x = sol.x # Obtiene el vector de X asociado al valor de Z

            if self.revisar_solucion(self.x): # Revisa la solucion factibe si es entera o no
                self.estado = "Solucion Factible Entera"                
            else:
                self.estado = "Solucion Factible No Entera"

            self.codigo = 0


    def revisar_solucion(self, arr):
        """Permite verificar si los X del problema son enteros"""

        for elem in arr: # Recorre el vector de solucion X
            if np.abs(np.floor(elem) - elem) > 0: # Si uno de los elementos en el vector no es entero, retorna falso
                return False
        return True # Retorna verdadero si todos los elementos son enteros


    def imprimir_modelo_PL(self):
        """Genera la informacion del problema de programacion lineal
            Muestra en forma de texto la funcion objetivo y restricciones
        """

        # Creando los datos para la funcion objetivo
        data = self.fo.get_tipo_opt(self.tipo_optimizacion)+" Z = "
        c = self.fo.get_funcion_objetivo()
        
        
        for i in range(0,self.num_variables):
            if c[i] < 0:
                data = data + str(c[i]) +"x"+str(i+1)
            else:
                if i > 0:
                    data = data + " + " + str(c[i]) +"x"+str(i+1)
                else:
                    data = data + str(c[i]) +"x"+str(i+1)

        restr_data = "s.a.\n"
        # Creando los datos para las restricciones
        for i in self.lista_restricciones:
            temp = i.get_lado_izquierdo()
            ctr = 0
            for j in temp:
                
                if j < 0:
                    restr_data = restr_data + str(j) +"x"+str(ctr+1)
                else:
                    if ctr > 0:
                        restr_data = restr_data + " + " + str(j) +"x"+str(ctr+1)
                    else:
                        restr_data = restr_data + str(j) +"x"+str(ctr+1)
                ctr = ctr + 1
            restr_data = restr_data + " " + i.ver_signo(i.get_tipo()) + " " + str(i.get_valor())
            restr_data = restr_data + "\n"
        restr_data = restr_data + "xi ≤ 1\n xi ≥ 0\n"
        
        return data+"\n"+restr_data

    def actualizar_profundidad(self):
        """
            Actualiza el valor de profundidad de un problema
            Sirve para determinar cual es la variable con la 
            cual se ramifica
        """
        self.profundidad = self.profundidad + 1

    def actualizar_descripcion(self,valor):
        """
            Agrega una descripción a un subproblema de programación lineal
            por ejemplo x_2 = 0
        """
        self.descripcion = "x"+str(self.profundidad)+" = " + str(valor)
        
        
    def get_estado(self):
        """Retorna el mensaje de estado del problema de programacion lineal"""
        return self.estado

    def get_codigo(self):
        """Retorna el codigo mediante el cual se conoce si el problema resuelto es factible o no """
        return self.codigo

    def get_profundidad(self):
        """Retorna el valor de profundidad para la ramificacion"""
        return self.profundidad

    def get_z(self):
        """Retorna el valor del Z de la f.o."""
        return self.z
    def get_x(self):
        """Retorna el valor que toman las variables en la f.o y restricciones"""
        return self.x
    def get_descripcion(self):
        """Retorna la descripcion del problema"""
        return self.descripcion
    def get_padre(self):
        """Retorna el identificador del subproblema padre"""
        return self.padre
    def get_id(self):
        """Retorna el identificador propio del subproblema"""
        return self.id

    def set_padre(self,padre):
        """Asigna el identificador del subproblema padre al subproblema"""
        self.padre = padre
    def set_id(self, id_modelo):
        """Asigna el identificador del subproblema"""
        self.id = id_modelo