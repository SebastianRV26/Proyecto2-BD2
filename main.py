from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
import os
import psycopg2
import json

# global variables
user = ""

# Cambiar de ventana.
def toBack (currentWindow, nextWindow):
        currentWindow.destroy()
        nextWindow.deiconify()

# Crear conección.
def createConnection(user, password, server, port, db):
    # user = user
    user = "basesII" # delete later
    try:
        # Está quemado, cambiarlo por los parametros
        conn = psycopg2.connect(user = "basesII",
                                password = "12345",
                                host = "leoviquez.com",
                                port = "5432",
                                database = "basesII")
        return conn
    except (Exception, psycopg2.Error) as error :
        print ("Error conectando a PostgreSQL", error)
        return None

# Validar connección.
def validateConnection(root, user, password, server, port, db):
    connection = createConnection(user, password, server, port, db)
    if (connection != None):
        secondWindow(root, connection)

# Mostrar plan de ejecución.
def showPlain(conn, text, context):
    cursor = conn.cursor()       
    consulta = text
    cursor.execute("explain (format JSON, " + context + ")" + consulta)
    result = cursor.fetchone()
    file = open(r"explain.json","wt")
    file.write(json.dumps(result[0]))
    file.close()
    os.system("python json_viewer.py explain.json")

# Ventana de privilegios
def privilegeWindow(root, connection):
    root.withdraw()
    window = Tk()
    window.config (background="gray")
    window.title("Privilegios")
    window.geometry ("1200x800")

    Label (window, text="Tablas", font="Arial, 12").pack()
    cmbTables = Combobox(window, font="Arial, 12")
    cmbTables.pack()
    cursor = connection.cursor()
    cursor.execute("""SELECT table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema NOT IN ('pg_catalog', 'information_schema');""") # Get tables
    result = cursor.fetchall() 
    #print(result)

    # cmbTables["values"] = []
    columns = []
    for i in result:
        columns.append(i[0])

    cmbTables["values"] = tuple(columns)
    cmbTables.current(0) #set the first item

    Label (window, text="Atributos", font="Arial, 12").pack()
    cmbAttributes = Combobox(window, font="Arial, 12")
    cmbAttributes.pack()
    
    def callback(eventObject):
        x = cmbTables.get()
        table = x
        cursor.execute("""SELECT column_name
        FROM information_schema.columns
        WHERE "table_name"='"""+table+"""'""") # Get tables
        result = cursor.fetchall() 
        columns = []
        for i in result:
            columns.append(i[0])
        cmbAttributes["values"] = tuple(columns)
        cmbAttributes.current(0)

    cmbTables.bind("<<ComboboxSelected>>", callback) # on item clicked

    btn_destroy = Button(window, text="Atrás", font="Arial, 12", command = lambda:toBack(window, root))
    btn_destroy.pack()

    root.wait_window(window)

# Ventana de planes de ejecición
def secondWindow(root, connection):
    root.withdraw()
    window = Tk()
    window.config (background="gray")
    window.title("Información")
    window.geometry ("1200x800")

    T = ScrolledText(window, height=10, width=100)
    T.pack(pady=10)
    T.insert(tk.END, """--Inserte aquí su código SQL para mostrar el plan de ejecución
    --código de ejemplo:
    select * from 
        optimizacion.catastro_municipal as c
        inner join
        optimizacion.patentes as p 
        on st_contains(c.geom,p.geom5367)
                    """)
    
    btn_plainTrue = Button(window, text="Ver el plan de ejecución estimado detallado", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "verbose true"))
    btn_plainTrue.pack()

    btn_plainFalse = Button(window, text="Ver el plan de ejecución estimado simple", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "verbose false"))
    btn_plainFalse.pack(pady=10)

    btn_plainRealTrue = Button(window, text="Ver el plan de ejecución real detallado", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "analize true"))
    btn_plainRealTrue.pack()

    btn_plainRealFalse = Button(window, text="Ver el plan de ejecución real simple", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "analize false"))
    btn_plainRealFalse.pack(pady=10)

    btn_privilege = Button(window, text="Ver privilegios", font="Arial, 12", command = lambda:privilegeWindow(window,connection))
    btn_privilege.pack()

    btn_destroy = Button(window, text="Cerrar sesión", font="Arial, 12", command = lambda:toBack(window, root))
    btn_destroy.pack(pady=10)

    root.wait_window(window)

# Ventana principal: Inicio de sesión.
def main():
    root = Tk()
    root.config (background="gray")
    root.title("Login")
    root.geometry ("1200x800")

    Label (root, text="Base de datos", font="Arial, 12").pack()
    entry_db = Entry(root, font="Arial, 12")
    entry_db.pack()

    Label (root, text="Servidor", font="Arial, 12").pack()
    entry_server = Entry(root, font="Arial, 12")
    entry_server.pack()

    Label (root, text="Puerto", font="Arial, 12").pack()  
    entry_port = Entry(root, font="Arial, 12")
    entry_port.pack()

    Label (root, text="Usuario", font="Arial, 12").pack() 
    entry_user = Entry(root, font="Arial, 12")
    entry_user.pack()

    Label (root, text="Contraseña", font="Arial, 12").pack() 
    entry_password = Entry(root, show="*", font="Arial, 12")
    entry_password.pack()
    
    btn_login=Button (root, text="Ingresar", font="Arial, 12", command = lambda:validateConnection(root,entry_user.get(), entry_password.get(), entry_server.get(), entry_port.get(), entry_db.get()))
    btn_login.pack()

    root.mainloop()

main()
