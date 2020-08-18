class FuncionObjetivo:
  """
    Clase que representa la función objetivo
    en un modelo de programación lineal
  """
  def __init__(self,fo):
    self.fo = fo # Vector que representa la funcion objetivo
    self.opt = { # Diccionario para determinar si se maximiza o minimiza la f.o
          1  :  "MIN",
          -1 :  "MAX"
    }


  def get_funcion_objetivo(self):
    """Retorna el vector que representa la funcion objetivo"""
    return self.fo
  def get_tipo_opt(self,valor):
    """Retorna el tipo de optimizacion (MIN|MAX)"""
    return self.opt[valor]