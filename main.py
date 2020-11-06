from tkinter import *
import os
import psycopg2
import json

def verPlan(user, password, server, port, db):
    try:
        conn = psycopg2.connect(user = user,
                                password = password,
                                host = server,
                                port = port,
                                database = db)
    except (Exception, psycopg2.Error) as error :
        print ("Error conectando a PostgreSQL", error)

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
    
    btn_login=Button (root, text="Ingresar", font="Arial, 12", command = lambda:verPlan(entry_user.get(), entry_password.get(), entry_server.get(), entry_port.get(), entry_db.get()))
    btn_login.pack()

    root.mainloop()

main()