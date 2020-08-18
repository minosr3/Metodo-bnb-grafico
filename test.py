"""from Modelo import *

a = Modelo(5)

a.agregar_producto("Queso2",1,3)
a.agregar_producto("Queso2",1,3)
a.agregar_producto("Queso2",1,3)
a.agregar_producto("Queso2",1,3)


a.solucion()
"""

from FuncionObjetivo import FuncionObjetivo
from Restriccion import Restriccion
from ModeloPL import ModeloPL
from Modelo import Modelo
from graphviz import Digraph,Source

#a = ModeloPL(3,-1)
#fo = FuncionObjetivo([1,2,-3])
#r1 = Restriccion([20,5,-1],10,1)
#r2 = Restriccion([12,3,-4],13,1)
#r3 = Restriccion([1,0,0],1,0)


a = ModeloPL(5,-1)
fo = FuncionObjetivo([100,150,200,100,50])
r1 = Restriccion([40,15,20,10,5],35,1)
#r2 = Restriccion([12,3,-4],13,1)
#r3 = Restriccion([1,0,0],1,0)


a.agregar_func_obj(fo)
a.agregar_restriccion(r1)
#a.agregar_restriccion(r2)
#a.agregar_restriccion(r3)

#print(a.imprimir_modelo_PL())

#print(a.get_tipo_optimizacion())
#print(a.crear_fo())
#print(a.crear_restricciones())

#a.resolver()
#print(a.z)
#print(a.x)
#print(a.estado)

m = Modelo(a)
m.generar_solucion()

#print(m.x_best)
#print(m.z_best)

for x in m.modelos:
    print( str(x.get_padre()) + ": "+ str(x.get_id()))

print(m.imprimir_modelos())
#print(m.get_x_best())
#print(m.get_z_best())