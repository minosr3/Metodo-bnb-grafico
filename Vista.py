from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from Nodo_GUI import *

class Ventana():
    """
        Vista del MVC
        Ventana principal del programa
    """

    def __init__(self):
        #Configuracion ventana
        self.ventana = Tk()    
        self.ventana.protocol("WM_DELETE_WINDOW",self.ventana.destroy)    
        self.ventana.title("Programacion entera binaria")
        self.ventana.geometry('800x800')
        self.ventana.resizable(width = False, height = False)

        self.ventana_diagr = None


        self.opt = { # Representacion de minimizacion o maximizacion
            "MIN" : 1,
            "MAX" : -1
        }

        self.signos = { # Representacion de signos de desiguladad o igualdad 
            "≤"  : 1,
            "≥"  : -1,
            "=" : 0
        }

        self.matriz_restr = [] # Matriz de entrada de restricciones
        self.fo = [] # Matriz de entrada para funcion objetivo
        self.signos_restricciones = [] # Matriz de emntrada para signos de igualdad o desigualdad 
        self.lado_derecho = [] # Matriz de entrada para lado derecho de las restricciones

        #Presentacion
        cristhian = Label(self.ventana, text = "Cristhian Camilo Martinez Rey - 20181020021", width = 40, font = ("Helvetica","10"))
        cristhian.pack(anchor = CENTER)
        alejandro = Label(self.ventana, text = "Brayan Alejandro Puentes - 20181020044", width = 40, font = ("Helvetica","10"))
        alejandro.pack(anchor = CENTER)
        brayan = Label(self.ventana, text = "Jose Alejandro Pintor Gonzales - 20152020054", width = 40, font = ("Helvetica","10"))
        brayan.pack(anchor = CENTER)
        
        #Labels
        self.variables = Label(self.ventana, text = "Variables:",width = 15, font=("Helvetica","15"))
        self.variables.pack(anchor = NW)
        self.restricciones = Label(self.ventana, text = "Restricciones:", width = 15, font = ("Helvetica","15"))
        self.restricciones.pack(anchor = NW)

        self.label_variables = [] # Label para mostrar x_1,x_2,... en la pantalla

        #Entradas
        self.num_variables = ttk.Entry(self.ventana,width=5)
        self.num_variables.place(x=150,y=72)
        self.num_restricciones = ttk.Entry(self.ventana,width=5)
        self.num_restricciones.place(x=150,y=102)

        self.tipo_opt = None # Almacena el tipo de optimizacion en combobox


        #Boton
        self.boton = ttk.Button(self.ventana, text = "Crear Modelo")
        self.boton.place(x=300, y=100)
        
        self.btn_restricciones = ttk.Button(self.ventana, text = "Consultar Datos Restricciones")
        #self.btn_restricciones.place(x=50, y=450)
        #self.btn_restricciones.bind("<Button>",self.getPesos)


        self.btn_lado_der = ttk.Button(self.ventana, text = "Consultar Datos Lado Derecho")
        #self.btn_lado_der.place(x=200, y=450)

        #Boton para hacer el cálculo
        self.btnCalcular = ttk.Button(self.ventana, text = "Resolver Problema")
        #self.btnCalcular.place(x=400, y=450)


        #Frame
        frame = Frame(self.ventana)
        frame.pack()

    
    def crearTabla(self):
        """ Permite crear las entradas de funcion objetivo y restricciones 
            para capturar el modelo de programación entera binaria
        """
        
        x1 = 0
        y1 = 0

        dx = 40
        dy = 30

        if not self.num_variables.get() or not self.num_restricciones.get():
            MessageBox.showerror("ERROR", "Por favor llene los espacios")
        else:
            try:
                valornum_variables = int(self.num_variables.get())
                valornum_restricciones = int(self.num_restricciones.get())
                if valornum_variables <= 0:
                    MessageBox.showerror("ERROR", "Por favor, el numero de variables debe ser positivo")
                elif valornum_restricciones <= 0:
                    MessageBox.showerror("ERROR", "Por favor, la cantidad de restricciones debe ser positiva")
                else:
                    
                    # Coloca el Combobox de minimizar o maximizar modelo
                    self.tipo_opt = ttk.Combobox(self.ventana,width=5)
                    self.tipo_opt.place(x=5,y=200)
                    self.tipo_opt['values'] = ["MIN","MAX"]
                    self.tipo_opt.current(1)
                    self.tipo_opt['state'] = "readonly"

                    #Coloca el label de Z = en pantalla
                    peso = ttk.Label(self.ventana, text = "Z = ", width = 5, font=("Helvetica","11"))
                    peso.place(x=60,y=200)
                    
                    #Coloca el label de sujeto a en pantalla
                    articulo = ttk.Label(self.ventana, text = " s.a. ", width = 5, font=("Helvetica","11"))
                    articulo.place(x=10,y=250)
                    
                    #Destruye las entradas y vacia cuando se cambian el numero de variables y restricciones
                    if len(self.matriz_restr) > 0:

                        for x in self.matriz_restr:
                            for r in x:
                                r.destroy()
                        for y in self.fo:
                            y.destroy()
                        for z in self.signos_restricciones:
                            z.destroy()
                        for w in self.lado_derecho:
                            w.destroy()
                        for t in self.label_variables:
                            t.destroy()
                        
                        self.label_variables = []
                        self.matriz_restr = []
                        self.signos_restricciones = []
                        self.lado_derecho = []
                        self.fo = []

                    x1 = 0
                    num_var = 1
                    # Crea y posiciona los label de variables xi en pantalla
                    for x in range(int(self.num_variables.get())):                       
                        
                        texto = "x"+str(num_var)
                        temp = Label(self.ventana, text = texto,width = 5, font=("Helvetica","10"))
                        temp.place(x=(85+x1), y= 180)
                        
                        self.label_variables.append(temp)
                        num_var = num_var + 1
                        x1 += dx

                    x1 = 0


                    # Crea y posiciona las entradas para funcion objetivo en pantalla
                    for x in range(int(self.num_variables.get())):
                        temp = ttk.Entry(self.ventana, width = 5)
                        temp.place(x=90+x1, y= 200+y1)
                        self.fo.append(temp)
                        x1 += dx

                    x1 = 0

                    # Crea y posiciona las entradas para lado izquierdo de las restricciones
                    for x in range(int(self.num_restricciones.get())):
                        temp_restric = []
                        for y in range(int(self.num_variables.get())):
                                temp = ttk.Entry(self.ventana, width = 5)
                                temp.place(x=90+x1, y= 250+y1)
                                temp_restric.append(temp)                                
                                x1 += dx                 
                        self.matriz_restr.append(temp_restric)                                    
                        x1 = 0
                        y1 += dy



                        

                    x1 = 90+(int(self.num_variables.get()))*dx
                    y1 = 250
                    # Crea y posiciona las entradas para signos de las restricciones
                    for y in range(int(self.num_restricciones.get())):
                        temp = self.crear_combobox_operador(x1,y1)
                        self.signos_restricciones.append(temp)
                        y1 += dy               


                      
                    x1 = 90+(int(self.num_variables.get())+1)*dx
                    y1 = 0
                    # Crea y posiciona las entradas para lado derecho de las restricciones
                    for y in range(int(self.num_restricciones.get())):
                        temp = ttk.Entry(self.ventana, width = 5)
                        temp.place(x=x1, y= 250+y1)
                        self.lado_derecho.append(temp)
                        y1 += dy               
                    

            except ValueError:
                MessageBox.showerror("ERROR", "Por favor, ingrese valores enteros positivos")

    
    def ocultar_botones(self):
        """
            Oculta los botones de la interfaz
            cuando no se tiene numero de variables
            ni numero de restricciones        
        """
        self.btn_restricciones.place_forget()
        self.btn_lado_der.place_forget()
        self.btnCalcular.place_forget()
    
    def mostrar_botones(self):
        """
            Muestra los botones de la interfaz
            cuando ya se tiene numero de variables
            y numero de restricciones
        """
        self.btn_restricciones.place(x=500, y=80)
        #self.btn_restricciones.bind("<Button>",self.getPesos)


        self.btn_lado_der.place(x=500, y=120)

        #Boton para hacer el cálculo
        self.btnCalcular.place(x=500, y=160)
            


    def crear_combobox_operador(self,pos_x,pos_y):
        """
            Crea el Combobox para los signos de
            las restricciones en la vista
            en una posicion x,y dada
        """
        combo = ttk.Combobox(self.ventana,width=1) # Crea el combobox
        combo.place(x=pos_x,y=pos_y) # Asigna el combobox a un x,y
        combo['values'] = ["≤","≥","="] # Asigna los posibles valores a tener en cuenta
        combo.current(0) # Asigna el valor por defecto
        combo['state'] = "readonly" # Solo lectura. No se puede modificar. Solo seleccionar

        return combo
    
    def mostrar_mensaje_error(self,mensaje):
        """Muestra un mensaje de error con el 
           mensaje del usuario
        """
        MessageBox.showerror("Error",mensaje)

    def crear_diagrama(self,modelo,padre,id_mod,msg,z,x,descrip,x_best,z_best):
        """Permite dibujar la estructura árbol con los datos de la clase
           Modelo mediante un objeto de la clase Nodo_GUI
        """
        temp = Nodo_GUI(modelo,padre,id_mod,msg,z,x,descrip,x_best,z_best)
        temp.dibujar()  
        #self.ventana_diagr = VistaDiagrama(temp)

    def validar_fo(self):
        """Valida si los elementos ingresados en la seccion de funcion objetivo son correctos"""
        try:
            for x in self.fo:
                float(x.get())
            return True            
        except ValueError:
            #MessageBox.showerror("ERROR", "Por favor, ingrese valores válidos en la función objetivo")
            return False
            


    def validar_restriccion(self):
        """Valida si los elementos ingresados en la seccion de lado izquierdo de restricciones son correctos"""

        try:
            for x in self.matriz_restr:
                for y in x:
                    float(y.get())
            return True            
        except ValueError:
            #MessageBox.showerror("ERROR", "Por favor, ingrese valores válidos en la matriz de restricciones")
            return False
            

    def validar_lado_derecho(self):
        """Valida si los elementos ingresados en la seccion de lado derecho de la descripcion son correctos"""
        try:
            for x in self.lado_derecho:
                float(x.get())
            return True            
        except ValueError:
            #MessageBox.showerror("ERROR", "Por favor, ingrese valores válidos en el lado derecho de las restricciones")
            return False
    

    def get_num_variables(self):
        """Retorna el numero de variables en la vista"""
        return int(self.num_variables.get())

    def get_num_restricciones(self):
        """
        Retorna el numero de restricciones en la vista
        """
        return int(self.num_restricciones.get())

    def get_tipo_optimizacion(self):
        """Retorna el tipo de optimizacion de la vista mediante numero
            1 MIN
           -1 MAX
        """
        return self.opt[self.tipo_opt.get()]

    def get_funcion_obj(self):
        """Retorna los datos de funcion objetivo de la vista"""
        fo = []

        for x in self.fo:
            temp = float(x.get())
            fo.append(temp)
        return fo

    def get_signos_restriccion(self):
        """Retorna los datos de signos de la restriccion en la vista
           Para cada elemento en el arreglo se retorna
            1 <=
            -1 >=
            0 =
        """
        arr_signos = []

        for x in self.signos_restricciones:
            temp = self.signos[x.get()]
            arr_signos.append(temp)
        return arr_signos

    def get_matriz_restriccion(self):
        """Retorna los datos del lado izquierdo de la restriccion en la vista"""
        data = []
        for x in self.matriz_restr:
            row = []
            for y in x:
                row.append(float(y.get()))
            data.append(row)
        return data 

    def get_lado_derecho(self):
        """Retorna los datos del lado derecha de la restriccion en la vista"""
        data = []
        for x in self.lado_derecho:
            data.append(float(x.get()))
        return data