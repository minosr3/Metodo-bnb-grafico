from graphviz import Digraph
class Nodo_GUI:
    """
        Clase para graficar el arbol de solucion
        de programacion entera binaria mediante
        Graphviz
    """
    def __init__(self,modelo = [],padre = [],id_mod = [],msg = [],z = [],x = [],descrip = [], x_best = [], z_best = []):
        self.modelo = modelo
        self.padre = padre
        self.id_mod = id_mod
        self.msg = msg
        self.z = z
        self.x = x
        self.descrip = descrip
        self.x_best = x_best
        self.z_best = z_best 

    def get_modelo(self):
        """Retorna los datos del modelo de programación lineal"""
        return self.modelo
    def get_padre(self):
        """Retorna el identificador del subproblema padre en la estructura árbol de Modelo"""
        return self.padre
    def get_id_mod(self):
        """Retorna el identificador del subproblema en la estructura árbol de Modelo"""
        return self.id_mod
    def get_msg(self):
        """Retorna el estado del subproblema"""
        return self.msg
    def get_z(self):
        """Retorna los valores de Z para cada subproblema de Modelo"""
        return self.z
    def get_x(self):
        """Retorna los valores de xi que obtienen el mejor Z en cada elemento de Modelo"""
        return self.x
    def get_x_best(self):
        """Retorna el conjunto de valores xi que genera el mejor Z en el problema"""
        return self.x_best
    def get_z_best(self):
        """Retorna el valor optimo de Z en el problema"""
        return self.z_best

    def dibujar(self):
        """
            Genera una gráfica SVG 
            donde se muestra todo el problema de programación binaria

        """
        g = Digraph('G', filename='hello.gv') # Crea la estructura de grafo
        g.format = 'svg' # Da el formato svg
        
        #g.attr('graph',label="Programación Binaria \n Z* = "+str(self.z_best)+"\n X="+str(self.x_best))

        texto_final = "Programación Binaria \n Z* = "+str(self.z_best)+"\n" #Texto para mostrar la solucion final
        for i in self.x_best:
            texto_final = texto_final+ "X = "+str(i)+"\n" # Agrega los vectores de X asociados al mejor valor de Z
        
        g.attr('graph',label=texto_final) # Agrega el texto_final al grafo como etiqueta


        g.attr()
        g.node("0",label=self.modelo[0]+"\n Z="+str(self.z[0])+"\n X="+str(self.x[0])) # Crea el nodo raiz, cuyo contenido es el modelo PL relajado inicial, Z y X
        for i in range(1,len(self.modelo)): # Agrega los nos de los demas subproblemas
            texto = self.msg[i] # Estado del subproblema

            if texto == "Solucion Factible Entera" or texto == "Solucion Factible No Entera": # Si la solucion es factible, muestra el valor de Z y X
                texto = texto +"\n Z="+str(self.z[i])+"\n X="+str(self.x[i])    
            else: # Si no es factible
                texto = texto + "\n\n"        

            g.node(str(self.id_mod[i]),label=texto) # Crea el nodo con la informacion de texto           
        
        for i in range(1,len(self.modelo)): # Crea las aristas con los nodos creados anteriormente utilizando el id de subproblema padre y el id propio del subproblema
            g.edge(str(self.padre[i]),str(self.id_mod[i]),label=self.descrip[i])

        g.view() # Grafica el arbol