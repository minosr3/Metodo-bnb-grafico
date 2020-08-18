class Restriccion:
    """Clase que representa una restriccion en un modelo de programación lineal"""

    def __init__(self,restriccion,valor,tipo = 1): 		
        self.lado_izquierdo = restriccion
        self.valor = valor # Lado derecho
        self.tipo = tipo # Signo de la restriccion 
        self.signos = { 1  : "≤",-1 : "≥",0 : "="} #Diccionario para determinar el signo de la restriccion en el modelo

    def get_lado_izquierdo(self):
        """Retorna el vector que representa la restriccion en su lado izquierdo"""
        return self.lado_izquierdo
    def get_valor(self):
        """Retorna el valor de la restriccion en su lado derecho"""
        return self.valor
    def get_tipo(self):
        """Retorna el signo que tiene la restriccion en forma numerica"""
        return self.tipo      
    def ver_signo(self,valor):
        """Retorna el caracter que representa al signo de la restriccion en forma numerica"""
        return self.signos[valor]