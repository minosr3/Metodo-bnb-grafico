from Controlador import Controlador
from Vista import Ventana
from Modelo import Modelo

class programacionBinaria():
    def __init__(self):
        v = Ventana()
        m = Modelo()
        c = Controlador(v,m)

def main():
    programacionBinaria()
    return 0

if __name__ == '__main__':
    main()
