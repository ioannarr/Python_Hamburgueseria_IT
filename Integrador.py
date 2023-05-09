#importo dos librerias, la primera para que haya tiempos de espera para los input del usuario y la segunda para represetar en tabla el pedido, y los datos del encargado

import time 
import sqlite3
import os

#importamos una libreria para mostrar los datos en forma de tabla

from tabulate import tabulate

#importamos las libreriras de tkinter para la interfaz grafica.

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font

#usando tkinter hacemos la interfaz para el usuario

ventana = tk.Tk()
ventana.title("Hamburgueseria IT")
ventana.geometry("400x450")
ventana.config(bg="lightgrey")


#creo una tabla y conecto la base de datos de sqlite.

def chequear():
    conn = sqlite3.connect("basededatos.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "CREATE TABLE ventas (Cliente TEXT, ComboSimple INT, ComboDoble INT, ComboTriple INT, Postre INT, Total REAL)"
        )
        cursor.execute(
             "CREATE TABLE registro (Evento TEXT, Encargado TEXT, Fecha TEXT, Caja REAL)"
        )
        print("Bienvenido por primera vez")
    except sqlite3.OperationalError:
        print("Bienvenido nuevamente")
    conn.commit()
    conn.close()



#validamos los ingresos del usuario que sean numeros

def validar(dato):
	try:
		dato = int(dato)
		return dato
	except ValueError:
		return -1


#para que sea mas grande y clar la letra de la pantalla

myfont = font.Font( family = "Verdana", size = 10, weight = "bold")


#agregamos funcionalidad al boton de salir  para el usuario para salir de la aplicacion.

def salir():
    salir = messagebox.showinfo(title='salir', message="Desea salir del progrma?")
    if salir:
        ventana.destroy()
    else:
      return


#agregamos funcionalidad al boton de borrar para el usuario para borrar los datos y poner nuevos.

def borrar():
    valor_simple.delete(0, tk.END)
    valor_doble.delete(0, tk.END)
    valor_triple.delete(0, tk.END)
    valor_postre.delete(0,tk.END)



#creo un objeto vacio como diccionario para representar los datos del el turno y lo facturado en caja por encargadao

turno = {'estado': 'OUT',
         'encargado':'', 
         'entrada': '',
         'caja': 0
         }

#agregamos funcionalidad al boton de pedido para que el usuario haga su pedido

def hago_pedido():
    
    mi_pedido = {}

    print('Estos son los Combos en Hambueseria IT: ')
        
    table = [['Hamburguesa simple + Bebida + Fritas', 300], ['(Hamburguesa doble + Bebida + Fritas', 400], ['Hamburguesa Triple + Bebida + Fritas', 450], ['Flurby', 100]]
    headers = ['Producto', 'Precio']

    print( tabulate(table,headers, tablefmt='pretty'))
  
    simple = valor_simple.get()
    simple = validar(simple)
    doble = valor_doble.get()
    doble = validar(doble)
    triple = valor_triple.get()
    triple = validar(triple)
    postre = valor_simple.get()
    postre = validar(postre)
    Cliente = valor_cliente.get()

    mi_pedido['Combo Simple']=simple
    mi_pedido['Combo Doble']=doble    
    mi_pedido['Combo Triple']=triple
    mi_pedido['Postre']=postre

    simple_total = simple * table[0][1]
    doble_total = doble * table[1][1]
    triple_total = triple * table[2][1]
    postre_total = postre * table[3][1]
    
    gran_total = int(simple_total + doble_total + triple_total + postre_total)
  
    print(f'El total de su pedido es de: {gran_total}')

    muestro = messagebox.showinfo(title="A pagar", message="$"+str(gran_total))
    
    if muestro:
        turno['caja'] += gran_total
        borrar()
        #usamos la importacion para imprimir en pantalla en forma de tabla      
        headers2 = ['Concepto', 'Valor']
        mi_pedido_tabla = list(map(list, mi_pedido.items())) 
        print( tabulate(mi_pedido_tabla, headers2, tablefmt='pretty'))

# volvemos a conectar a la base de datos para guardar el pedido

        conn = sqlite3.connect("basededatos.sqlite")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", (Cliente, simple, doble, triple, postre, turno['caja']))
        conn.commit()
        conn.close()
        print("Producto salvado con exito")

#abrimos y escribimos los datos de mi pedido dentro de un archivo txt que se llama Ventas:

        f = open('Ventas.text', 'a')
        datos = f.write(f'{mi_pedido}-{time.asctime()}' + '\n')
        print(datos)
        f.close()
    
    
    return mi_pedido




#Elaboramos la interfaz con los wiedgets de tkinter bajo el esquema de grid()

label1 =tk.Label(ventana, text='HAGA SU PEDIDO - Hamburgeseria IT ', font=myfont)
label1.grid(row= 1, column=0, columnspan=6, padx=5, pady=5, ipadx=5, ipady=5)

nombre_encargado =tk.Label(ventana, text='Nombre Encargado: ', font=myfont)
nombre_encargado.grid(row= 3, column=0, columnspan=3,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_encargado = tk.Entry(ventana, width= 20)
valor_encargado.grid(row=3, column=2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)

nombre_cliente =tk.Label(ventana, text='Nombre Cliente: ', font=myfont)
nombre_cliente.grid(row= 4, column=0, columnspan=3,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_cliente = tk.Entry(ventana, width= 20)
valor_cliente.grid(row=4, column=2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)

combo_simple =tk.Label(ventana, text='Combo Simple cantidad: ', font=myfont)
combo_simple.grid(row= 5, column=0, columnspan=2,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_simple= tk.Entry(ventana, width= 10)
valor_simple.grid(row=5, column= 2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)

combo_doble =tk.Label(ventana, text='Combo Doble cantidad: ', font=myfont)
combo_doble.grid(row= 6, column=0, columnspan=2,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_doble= tk.Entry(ventana, width= 10)
valor_doble.grid(row=6, column=2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)

combo_triple =tk.Label(ventana, text='Combo Triple cantidad: ', font=myfont)
combo_triple.grid(row= 7, column=0, columnspan=2,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_triple= tk.Entry(ventana, width= 10)
valor_triple.grid(row=7, column= 2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)

postre=tk.Label(ventana, text='Postre cantidad: ', font=myfont)
postre.grid(row= 8, column=0, columnspan=2,  sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=5)

valor_postre= tk.Entry(ventana, width= 10)
valor_postre.grid(row=8, column= 2, columnspan=2, sticky=tk.E, padx=5, pady=5, ipadx=5, ipady=5)


boton1 = tk.Button(ventana, text='HACER PEDIDO', font=myfont, command=hago_pedido)
boton1.grid(row=11, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5 )

boton3 = tk.Button(ventana, text='CANCELAR PEDIDO', font=myfont, command=borrar)
boton3.grid(row=11, column=2, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5 )

boton2 = tk.Button(ventana, text='SALIR', font=myfont, command=salir)
boton2.grid(row=12, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5 )



#Despliegue de Bienvenida

print('Bienvenido Colaborador de Hamburgueseria IT !!!')

#Despliegue de Menu, donde pido la opcion y decido por menu

def despliego_menu():
        
    # print('1 – Ingreso nuevo pedido')
    print('2 – Registro de Entrada')
    print('3 – Rgistro de Salida') 

    try:                       
        opcion = int(input('Ingrese una opcion 2 o 3 para continuar: '))
        
        if isinstance(2,int) or isinstance(3,int):
                print(f'Su opcion elegida es la: {opcion} ')
                valido_menu(opcion)
        
        else:
            print(f'Ingrese 2 o 3.... ')
        
    except (TypeError,ValueError):           
            print('Vuelva a intentarlo...')
           

#valido las opcionces de menu

def valido_menu(opcion):
      
    if opcion == 2:
#si ya hay una persona registrada entonces no puede registrarse otra vez
        if turno.get('estado') == 'IN':     
             print('Ingrese su salida seleccionando 3')
#si no hay nadie, lo dejamos registrarse con la funcion registro_entrada()
        else:
            print('Sistema de Registro de Empleados')
            registro_entrada()
    
    elif opcion == 3:
#si no hay empleado trabajando, no puede regustrar su salida, tiene que registrarse, 
        if turno.get('estado') == 'OUT':     
             print('Ingrese su entrada seleccionando 2')
        
        else:
#si hay alguien, lo dejamos irse con la funcion registro_salida()        
            registro_salida()
            print('Gracias por usar el Sistema de Pedidos')
     
    else:
#si ingresa un numero diferente alo que pide el menu, le pide un un re ingreso de los datos 
        print('Por favor ingrese una opcion dentro del menu: ')
    
#retornamos la opcion elegida para validar el menu 
    return opcion            






#Pedido datos den encargado para completar el dicionario de turno y poder guardarlo en regsitro.txt 

def registro_entrada():

#nombre de encargado, el timestamp y cambio el estado de OUT a IN y la caja la incializo en cero para cada nuevo encargado
    
    encargado = input('Ingrese su nombre de Encargado: ')
    turno['estado'] = 'IN'
    turno['encargado'] = encargado
    entrada = time.asctime()
    turno['entrada'] = entrada
    turno['caja'] = 0
    
    print(f'Bienvenido {encargado}, Recuerda, siempre hay que recibir al cliente con una sonrisa :)!')
   
#guardo los datos en un tabla de registros:

    try:
        conn = sqlite3.connect("basededatos.sqlite")
        cursor = conn.cursor()        
        cursor.execute("INSERT INTO registro VALUES (?, ?, ?, ?)", (turno['estado'],encargado, entrada,turno['caja']))
        conn.commit()
        conn.close()
        print("Resgistro salvado con exito")
    except sqlite3.OperationalError:
        print("No se puede guardar en este momento. Vuelva a intentarlo más tarde")

#creo y escribo el resgistro con el estado de In de registro de entrada en n archivo de Registro.txt:

    f = open('Registro.txt','a')
    registro_entrada = f.write(f' IN - {encargado}  - {entrada}' + '\n')
    print(registro_entrada)
    f.close()

#retorno el diccionario turno con los datos cargados:

    return turno

#Funcion que me registra la salida del encargado y le dejamos el turno en vacio para un nuevo registro de entrada. 
#Tambienle cambiamos el estado de IN a OUT y grabamos otra vez la salida con el nombre, y timestamp
#tambien traemos el dato de la caja gfacturada desde el diccionario turno

def registro_salida():
    
    turno['estado'] = 'OUT'
    print('Ud termino su dia de trabajo')
  
    f = open('Registro.txt','a') 
    registro_salida = f.write(f' OUT - {turno.get("encargado")} - {time.asctime()} - {turno.get("caja")}'  + '\n')
     
    print(registro_salida)
    f.close()
    turno['encargado'] = ''
    turno['caja'] = 0

########################################################

#esta es la ejecucion del programa donde constantemente cada vez que termina una funcion y no esta haciendo otra cosa:

chequear()

#me va a desplegar el menu de las tres opciones en pantalla:

while True:
    despliego_menu()





