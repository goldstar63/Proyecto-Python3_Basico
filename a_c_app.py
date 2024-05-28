from tkinter import ttk
from tkinter import *
import sqlite3
import re

almacen_db = 'almacen.db'

prod_old = ''
prov_old = ''
cant_old = 0
prec_old = 0
ubic_old = ''
tota_old = 0

# ##############################
#MODELO
# ##############################

def run_query(query, parametros=()):                      #Esta funcion me permite hacer consultas a la base de datos
    with sqlite3.connect(almacen_db) as conn:
        cursor = conn.cursor()                            #conn mediante cursor() me permite posicionarme en la BD
        result = cursor.execute(query, parametros)        #execute me permite ejecutar consultas SQL
        conn.commit()
    return result

def get_info():                                            #Esta funcion me permite obtener la info de la BD
    
    #cleaning table
    records = tree.get_children()                          #get_children me permite obtener toda la info que hay en tree
    for i in records:                                      #Con for recorro cada elemento de records y lo borro
        tree.delete(i)
    
    #quering data
    query = 'SELECT * FROM registroprod ORDER BY id DESC'
    db_rows = run_query(query)
    for r in db_rows:
        tree.insert('', 0, text=r[0], values=(r[1], r[2], r[3], r[4], r[5], r[6]))

def validacion():                                           #La funcion valida que los campos de entrada de la aplicacion no esten vacios. En ese caso retorna TRUE. En caso contrario retorna FALSE.
    return len(nprod1_entry.get()) != 0 and len(nprov1_entry.get()) != 0 and len(cantpr1_entry.get()) != 0 and len(precpr1_entry.get()) != 0 and len(ubicpr1_entry.get()) != 0 and len(valtot1_entry.get()) != 0


def func_insertar():
    
    if validacion():                                                                    #Valido antes de ingresar datos en la BD que todos los campos entry tengan informacion y que los campos de texto tengan texto y los de numeros tengan numeros.
        query = 'INSERT INTO registroprod(id, producto, proveedor, cantidad, precio, ubicacion, total) VALUES(NULL, ?, ?, ?, ?, ?, ?)'
        parametros = (nprod1_entry.get(), nprov1_entry.get(), cantpr1_entry.get(), precpr1_entry.get(), ubicpr1_entry.get(), valtot1_entry.get())
        run_query(query, parametros)
        mensaje['text'] = 'El producto {} fue ingresado'.format(nprod1_entry.get())     #format me permite acceder al dato que deseo escribir en {}
        nprod1_entry.delete(0, END)                                                     #Blanquea los campos de datos cuando finalice el ingreso del registro.
        nprov1_entry.delete(0, END)
        cantpr1_entry.delete(0, END)
        precpr1_entry.delete(0, END)
        ubicpr1_entry.delete(0, END)
        valtot1_entry.delete(0, END)
    
    else:
        mensaje['text'] = 'Registro no Ingresado. Por favor, complete todos los campos'

    get_info()


def func_eliminar():
                                             
    id = tree.item(tree.selection())['text']                                              #Con esto estoy tomando solo el valor del elemento text del diccionario (el id). Esto me permite conocer el registro a eliminar
    query = 'DELETE FROM registroprod WHERE id = ?'
    run_query(query, (id, ))
    mensaje['text'] = 'El producto {} fue eliminado'.format(id)

    get_info()


def func_buscar(nombprod):
    mensaje['text'] = ''

    patron = "^[a-z]*$"

    if (re.match(patron, nombprod)):
        #cleaning table
        records = tree.get_children()       #get_children() guardar toda la lista en records
        for i in records:
            tree.delete(i)
    
        #quering data
        query = 'SELECT * FROM registroprod WHERE producto = ?'
        db_rows = run_query(query, (nombprod, ))
        for r in db_rows:
            tree.insert('', 0, text=r[0], values=(r[1], r[2], r[3], r[4], r[5], r[6]))
    
        nomb_busc.delete(0, END)

    else:
        mensaje['text'] = 'Por favor, ingrese el nombre del producto en minuscula, sin espacio, numeros, ni caracteres especiales'


def func_modificar():

    global prod_old
    global prov_old
    global cant_old
    global prec_old
    global ubic_old
    global tota_old

    prod_old = tree.item(tree.selection())['values'][0]     #Guardamos los datos viejos del registro a modificar
    prov_old = tree.item(tree.selection())['values'][1]
    cant_old = tree.item(tree.selection())['values'][2]
    prec_old = tree.item(tree.selection())['values'][3]
    ubic_old = tree.item(tree.selection())['values'][4]
    tota_old = tree.item(tree.selection())['values'][5]

    mensaje['text'] = 'Los datos del registro seleccionado fueron tomados'


def func_aceptar(new_nomb, old_nomb, new_prov, old_prov, new_cant, old_cant, new_prec, old_prec, new_ubic, old_ubic, new_tot, old_tot):
        
    query = 'UPDATE registroprod SET producto = ?, proveedor = ?, cantidad = ?, precio = ?, ubicacion = ?, total = ? WHERE producto = ? AND proveedor = ? AND cantidad = ? AND precio = ? AND ubicacion = ? AND total = ?'
    parametros = (new_nomb, new_prov, new_cant, new_prec, new_ubic, new_tot, old_nomb, old_prov, old_cant, old_prec, old_ubic, old_tot)     #La tupla se organiza: Nuevos datos primero y viejos datos despues
    run_query(query, parametros)

    mensaje['text'] = 'El registro fue actualizado'

    nomb_nuevo.delete(0, END)
    prov_nuevo.delete(0, END)
    cant_nueva.delete(0, END)
    prec_nuevo.delete(0, END)
    ubic_nueva.delete(0, END)
    tot_nuevo.delete(0, END)
    
    get_info()

# ##############################
#VISTA - CONTROLADOR
# ##############################

#INICIA LA VENTANA WINDOWS

windows = Tk()
windows.title("ALMACEN CENTRAL")

#Creamos el Frame Container Datos del Producto

frame = LabelFrame(windows, text='Datos del Producto')
frame.grid(row=0, column=0, columnspan=3, pady = 20) #columnspan=3 dejo 3 columnas en blanco y pady = 20 doy un espaciado en el eje de las y de 20 pixeles.

#Creamos los elementos que van dentro del Frame Container

Label(frame, text="Nombre del Producto").grid(row=1, column=0)
nprod1_entry = Entry(frame)
nprod1_entry.grid(row=1, column=1)
nprod1_entry.focus()    #Cuando inicia la ventana el cursor se posiciona en este campo.

Label(frame, text="Nombre del Proveedor").grid(row=1, column=2)
nprov1_entry = Entry(frame)
nprov1_entry.grid(row=1, column=3)

Label(frame, text="Cantidad del Producto").grid(row=2, column=0)
cantpr1_entry = Entry(frame)
cantpr1_entry.grid(row=2, column=1)

Label(frame, text="Precio del Producto").grid(row=2, column=2)
precpr1_entry = Entry(frame)
precpr1_entry.grid(row=2, column=3)

Label(frame, text="Ubicacion del Producto").grid(row=3, column=0)
ubicpr1_entry = Entry(frame)
ubicpr1_entry.grid(row=3, column=1)

Label(frame, text="Valor Total de la Inversion").grid(row=3, column=2)
valtot1_entry = Entry(frame)
valtot1_entry.grid(row=3, column=3)

boton_insert = Button(frame, text="Insertar", command=func_insertar)
boton_insert.grid(row=4, columnspan=4, sticky = W + E)


#Creamos el Frame Container para Modificar el Producto

frame2 = LabelFrame(windows, text='Modificar Datos del Producto')
frame2.grid(row=5, column=0, columnspan=3, pady = 20)

Label(frame2, text="Nuevo Nombre").grid(row=5, column=0)
nomb_nuevo = Entry(frame2)
nomb_nuevo.grid(row=5, column=1)

Label(frame2, text="Nuevo Proveedor").grid(row=5, column=2)
prov_nuevo = Entry(frame2)
prov_nuevo.grid(row=5, column=3)

Label(frame2, text="Nueva Cantidad").grid(row=6, column=0)
cant_nueva = Entry(frame2)
cant_nueva.grid(row=6, column=1)

Label(frame2, text="Nuevo Precio").grid(row=6, column=2)
prec_nuevo = Entry(frame2)
prec_nuevo.grid(row=6, column=3)

Label(frame2, text="Nueva Ubicacion").grid(row=7, column=0)
ubic_nueva = Entry(frame2)
ubic_nueva.grid(row=7, column=1)

Label(frame2, text="Nuevo Total").grid(row=7, column=2)
tot_nuevo = Entry(frame2)
tot_nuevo.grid(row=7, column=3)

boton_modificar = Button(frame2, text="Modificar", command=func_modificar)
boton_modificar.grid(row=8, column=1)

boton_aceptar = Button(frame2, text="Aceptar", command=lambda:func_aceptar(nomb_nuevo.get(), prod_old, prov_nuevo.get(), prov_old, cant_nueva.get(), cant_old, prec_nuevo.get(), prec_old, ubic_nueva.get(), ubic_old, tot_nuevo.get(), tota_old))
boton_aceptar.grid(row=8, column=2)


#Creamos el Frame Container para Busquedas

frame3 = LabelFrame(windows, text='Busqueda de Productos')
frame3.grid(row=9, column=0, columnspan=3, pady = 20)

Label(frame3, text="Nombre del Producto").grid(row=10, column=0)
nomb_busc = Entry(frame3)
nomb_busc.grid(row=10, column=1)

boton_buscar = Button(frame3, text="Buscar", command=lambda:func_buscar(nomb_busc.get()))
boton_buscar.grid(row=10, column=2)

#Mensaje de Salida
mensaje = Label(text='', fg='blue')
mensaje.grid(row=11, column=0, columnspan=4, sticky = W + E)     #sticky me permite posicionar el label a todo lo largo de la fila.

#Creamos la Tabla con TreeView

tree = ttk.Treeview(windows)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=50, minwidth=50, anchor=W)
tree.column("col1", width=80, minwidth=80, anchor=W)
tree.column("col2", width=80, minwidth=80, anchor=W)
tree.column("col3", width=80, minwidth=80, anchor=W)
tree.column("col4", width=80, minwidth=80, anchor=W)
tree.column("col5", width=80, minwidth=80, anchor=W)
tree.column("col6", width=80, minwidth=80, anchor=W)

tree.grid(column=0, row=12, columnspan=3)
tree.heading("#0", text="Id", anchor=CENTER)    #Le colocamos los encabezados a la tabla
tree.heading("#1", text="Producto", anchor=CENTER)
tree.heading("#2", text="Proveedor", anchor=CENTER)
tree.heading("#3", text="Cantidad", anchor=CENTER)
tree.heading("#4", text="Precio", anchor=CENTER)
tree.heading("#5", text="Ubicacion", anchor=CENTER)
tree.heading("#6", text="Total_Inver", anchor=CENTER)

boton_eliminar = Button(windows, text="Eliminar", command=func_eliminar)
boton_eliminar.grid(row=13, columnspan=4, sticky = W + E)


#Barra Menu
menu_bar = Menu(windows)

menu_quit = Menu(menu_bar, tearoff=0)
menu_quit.add_command(label="Salir", command=windows.quit)
menu_bar.add_cascade(label="Salir", menu=menu_quit)

menu_listar = Menu(menu_bar, tearoff=0)
menu_listar.add_command(label="Listar", command=get_info)
menu_bar.add_cascade(label="Listar", menu=menu_listar)

windows.config(menu=menu_bar)


windows.mainloop()