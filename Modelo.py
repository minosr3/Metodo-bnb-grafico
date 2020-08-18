from ModeloPL import ModeloPL
from Restriccion import Restriccion
import copy as copy
class Modelo:
    """
    Clase para almacenar la estructura de árbol del
    problema de programación binaria
    """

    def __init__(self,original=None):
        self.z_best = None # Almacena el mejor valor de Z encontrado en el árbol
        self.x_best = None # Almacena los X que generan el mejor valor de Z
        self.id_best = -1

        self.original = original # Almacena el Modelo de PL original o relajado
        self.modelos = [] #Almacena modelos de PL y son los nodos del arbol



    def generar_solucion(self):
        """
        Resuelve el problema de programación binaria
        resolviendo subproblemas mediante el uso 
        de ramificación y acotamiento        
        """


        cola = [] # Cola donde se atiende cada uno de los subproblemas
        cola.append(self.original) # Se inicia resolviendo el problema de PL relajado

        id = 0


        while len(cola) > 0: # Mientras se tengan subcasos por resolver
            
            
            temp = cola.pop(0) # Desencola el problema de la cola
            temp.resolver() # Resuelve este subproblema
            temp.set_id(id) # Asigna un identificador de problema
            id = id + 1 
            self.modelos.append(temp)# Añade el problema a un lista de problemas resueltos

            if self.evaluar_soluciones(temp) == 1: # Si se tiene un problema con solucion factible entera, ramifique
                padre = temp.get_id() # Se obtiene el identificador
                temp_1 = copy.deepcopy(temp) # Copia del problema
                temp_2 = copy.deepcopy(temp) # Copia del problema
                

                if temp_1.get_profundidad() <= temp_1.get_numero_variables(): # Crea el nodo izquierdo, xi = 0 
                    temp_1.actualizar_profundidad() # Actualiza el valor de la profundidad en el árbol
                    temp_1.actualizar_descripcion(0) # Crea la descripcion del subproblema, es decir, xi = 0 
                    temp_1.set_padre(padre)
                    
                    r1 = self.generar_restriccion(temp_1.get_profundidad(),0,temp_1.get_numero_variables()) # Genera la restriccion xi = 0 o xi = 1 de acuerdo al valor de profundidad
                    temp_1.agregar_restriccion(r1) # Agrega la restricción al problema
                    cola.append(temp_1) # Encola el problema con la nueva restriccion

                

                if temp_2.get_profundidad() <= temp_2.get_numero_variables(): # Crea el nodo derecho, xi = 1               
                    temp_2.actualizar_profundidad() # Actualiza el valor de la profundidad en el árbol
                    temp_2.actualizar_descripcion(1)# Crea la descripcion del subproblema, es decir, xi = 1
                    temp_2.set_padre(padre)
                    
                    r2 = self.generar_restriccion(temp_2.get_profundidad(),1,temp_2.get_numero_variables()) # Genera la restriccion xi = 0 o xi = 1 de acuerdo al valor de profundidad
                    temp_2.agregar_restriccion(r2) # Agrega la restricción al problema
                    cola.append(temp_2) # Encola el problema con la nueva restriccion                               
            
            
            


    def evaluar_soluciones(self, elem):
        """
        Permite evaluar la solución y retorna un número
        que es un código para indicar si se tiene una solución
        entera, no entera o una solución no factible o no acotada"""
        
        
        estado = 0 # Codigo para conocer si la solución es factible o no
            
        if elem.get_codigo() == 0:                        
            if elem.get_estado()  == "Solucion Factible Entera":
                self.actualizar_solucion(elem.get_z(),elem.get_x(),elem.get_tipo_optimizacion())
                estado = 0 # Codigo que indica que la solución es entera
            elif elem.get_estado()  == "Solucion Factible No Entera":
                estado = 1 # Codigo que indica que la solución no es entera, que sirve para ramificar           
        else:
            estado = -1 # Código que indica que la solución es infactible 

        return estado


    def actualizar_solucion(self,z,x,tipo):
        """
        Permite actualizar a la mejor solución encontrada
        En las iteraciones del B&B
        """
        if self.z_best is None or self.x_best is None: # Si no hay ninguna solución, se agrega la solución
            self.z_best = z
            self.x_best = []
            self.x_best.append(x)
        else:
            if z < self.z_best and tipo == 1: # Actualiza el valor de z y el vector x en minimizacion
                self.z_best = z
                self.x_best = []
                self.x_best.append(x)                        
            if z > self.z_best and tipo == -1: # Actualiza el valor de z y el vector x en maximizacion
                self.z_best = z
                self.x_best = []
                self.x_best.append(x)

            
            if z == self.z_best: #En caso de encontrar otra solucion
                for elem in self.x_best: # Compara la solucion entrante con las que estan en x_best para añadirla o no
                    if list(elem) != list(x):
                        self.x_best.append(x)
                

                
            
    def generar_restriccion(self,profundidad,valor,num_variables):
        """Genera el vector que representa la restricción de la forma xi = 0 o xi = 1"""
        li = [1 if i+1==profundidad else 0 for i in range(num_variables)]

        return Restriccion(li,valor,0)
    
    def imprimir_modelos(self):
        """Imprime la estructura de arbol de programacion binaria """
        print(len(self.modelos))
        print(self.modelos)
        for i in range(0,len(self.modelos)):
            print("Modelo:" + str(i))
            if self.modelos[i].get_codigo() == 0:
                print(self.modelos[i].imprimir_modelo_PL()+self.modelos[i].get_estado()+"\nX ="+str(self.modelos[i].get_x())+"\nZ="+str(self.modelos[i].get_z())+"\n")
            else:
                print(self.modelos[i].imprimir_modelo_PL()+self.modelos[i].get_estado()+"\n")

    def get_datos_modelos(self):
        """
        Retorna los datos de los nodos del modelo
        @returns datos de los nodos
        """
        modelo = []
        padre = []
        id_modelo = []
        mensaje = []       
        descrip = [] 
        z = []
        x = []
        for i in self.modelos:
            mensaje.append(i.get_estado())
            modelo.append(i.imprimir_modelo_PL())
            padre.append(i.get_padre())
            id_modelo.append(i.get_id())
            z.append(i.get_z())
            x.append(i.get_x())
            descrip.append(i.get_descripcion())

        return modelo,padre,id_modelo,mensaje,z,x,descrip

    def get_z_best(self):
        """Retorna el valor del mejor valor de z o z_best"""
        return self.z_best
    def get_x_best(self):
        """Retorna las soluciones del problema o x_best"""
        return self.x_best