from FuncionObjetivo import FuncionObjetivo
from ModeloPL import ModeloPL
from Restriccion import Restriccion
class ArmadorModelo:
    """
        Clase Auxiliar para armar el modelo de PL
        a partir de las entradas de la vista
    """
    def __init__(self,num_vars,tipo,c,a,signo,b):
        self.num_vars = num_vars # numero de variables
        self.tipo = tipo # min o max
        self.c = c # funcion objetivo
        self.a = a # lado izquierdo de las restricciones
        self.signo = signo # signos <=, >= o = en las restricciones
        self.b = b # lado derecho de las restricciones
        
        

    
    def crear_fo(self):
        """Crea un objeto funcion objetivo a partir de la entrada"""
        return FuncionObjetivo(self.c)        
    def crear_restriccion(self):     
        """Crea la lista de objetos restricciones a partir de la entrada"""
        
        lista_restricciones = []   
        for i in range(0,len(self.a)):                   
            restr = Restriccion(self.a[i],self.b[i],self.signo[i])                       
            lista_restricciones.append(restr)            
        return lista_restricciones
    
    def generar_restriccion(self,lado_izq,signo,lado_der):
        """Genera una Restriccion para agregar al modelo de PL"""
        return Restriccion(lado_izq,lado_der,signo)

    def generar_modelo(self):
        """
        Crea un objeto ModeloPL que representa el modelo de PL
        con el número de variables y min|max elegida
        """
        m = ModeloPL(self.num_vars,self.tipo)
        m.agregar_func_obj(self.crear_fo())
        
        restr = self.crear_restriccion()

        for elem in restr:
            m.agregar_restriccion(elem)
        
        return m