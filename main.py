from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import psycopg2
import json

def toBack (currentWindow, nextWindow):
        currentWindow.destroy()
        nextWindow.deiconify()

def createConnection(user, password, server, port, db):
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

def validateConnection(root, user, password, server, port, db):
    connection = createConnection(user, password, server, port, db)
    if (connection != None):
        secondWindow(root, connection)
        
def showPlain(conn, text):
    cursor = conn.cursor()       
    consulta = text
    cursor.execute("""explain (format JSON, verbose true)                             
                            """+consulta)
    result = cursor.fetchone()
    file = open(r"explain.json","wt")
    file.write(json.dumps(result[0]))
    file.close()
    os.system("python json_viewer.py explain.json")

def secondWindow(root, connection):
    root.withdraw()
    window = Tk()
    window.config (background="gray")
    window.title("Información")
    window.geometry ("1200x800")

    T = ScrolledText(window, height=10, width=100)
    T.pack()
    T.insert(tk.END, """--Inserte aquí su código SQL para mostrar el plan de ejecución
    --código de ejemplo:
    select * from 
        optimizacion.catastro_municipal as c
        inner join
        optimizacion.patentes as p 
        on st_contains(c.geom,p.geom5367)
                    """)
    
    btn_plain = Button(window, text="Ver plan", command = lambda:showPlain(connection, T.get("1.0","end")))
    btn_plain.pack()

    btn_privilege = Button(window, text="Ver privilegio" """, command = lambda:showPlain(connection, T.get("1.0","end"))""")
    btn_privilege.pack()

    btn_destroy = Button(window, text="Cerrar sesión", command = lambda:toBack(window, root))
    btn_destroy.pack()

    root.wait_window(window)

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
