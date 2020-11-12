from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from tkinter import ttk
import os
import psycopg2
import json

class Table(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Privilegios de la tabla y sus atributos")
        
        self.treeview2 = ttk.Treeview(self, columns=("select", "insert", "update", "delete", "references", "trigger", "truncate"))
        self.treeview2.pack()
        self.treeview2.heading("#0", text="Atributo")
        self.treeview2.heading("select", text="Select")
        self.treeview2.heading("insert", text="Insert")
        self.treeview2.heading("update", text="Update")
        self.treeview2.heading("delete", text="Delete")
        self.treeview2.heading("references", text="References")
        self.treeview2.heading("trigger", text="Trigger")
        self.treeview2.heading("truncate", text="truncate")

        self.treeview = ttk.Treeview(self, columns=("select", "insert", "update", "references"))
        self.treeview.pack()
        self.treeview.heading("#0", text="Atributo")
        self.treeview.heading("select", text="Select")
        self.treeview.heading("insert", text="Insert")
        self.treeview.heading("update", text="Update")
        self.treeview.heading("references", text="References")
        
        self.pack()

    def set_rowTable(self, name, select, insert, update, delete, references, trigger, truncate):
        self.treeview2.insert("", tk.END, text=name, values=(select, insert, update, delete, references, trigger, truncate))

    def set_row(self, name, select, insert, update, references):
        self.treeview.insert("", tk.END, text=name, values=(select, insert, update, references))

# global variables
globalUser = ""

# Cambiar de ventana.
def toBack (currentWindow, nextWindow):
        currentWindow.destroy()
        nextWindow.deiconify()

# Crear conección.
def createConnection(user, password, server, port, db):
    # user = user
    global globalUser
    globalUser = "basesII" # delete later
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
    # Get scheme.tables
    cursor.execute("""SELECT table_schema || '.' || table_name AS table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
            AND table_schema NOT IN ('pg_catalog', 'information_schema');""")
    result = cursor.fetchall() 
    #print(result)

    # cmbTables["values"] = []
    columns = []
    for i in result:
        columns.append(i[0])

    cmbTables["values"] = tuple(columns)

    def callback(eventObject):
        x = cmbTables.get()
        items = x.split('.')

        window2 = Tk()
        table = Table(window2)
        
        cursor.execute("""select 
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'select') as select,
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'insert') as insert,
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'update') as update,
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'delete') as delete, 
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'references') as references,
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'trigger') as trigger,
            HAS_TABLE_PRIVILEGE('"""+globalUser+"""', '"""+items[1]+"""', 'truncate') as truncate
        from INFORMATION_SCHEMA.TABLES T
        WHERE T.TABLE_NAME='"""+ items[1] +"""' 
        AND T.table_schema = '""" + items[0] + """'""")
        i = cursor.fetchall()[0]

        table.set_rowTable(items[1] , str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]))

        cursor.execute("""select COLUMN_NAME, 
            has_column_privilege('"""+globalUser+"""', '"""+items[1]+"""', COLUMN_NAME, 'select') as select,
            has_column_privilege('"""+globalUser+"""', '"""+items[1]+"""', COLUMN_NAME, 'insert') as insert,
            has_column_privilege('"""+globalUser+"""', '"""+items[1]+"""', COLUMN_NAME, 'update') as update,
            has_column_privilege('"""+globalUser+"""', '"""+items[1]+"""', COLUMN_NAME, 'references') as references
        from INFORMATION_SCHEMA.COLUMNS C
        WHERE C.TABLE_NAME='"""+ items[1] +"""' 
        AND C.table_schema = '""" + items[0] + """'""")

        result = cursor.fetchall()         
        for i in result:
            # columns.append(i[0])
            table.set_row(i[0], str(i[1]), str(i[2]), str(i[3]), str(i[4]))

        table.mainloop()

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

    btn_plainRealTrue = Button(window, text="Ver el plan de ejecución real detallado", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "analyze false"))
    btn_plainRealTrue.pack()

    btn_plainRealFalse = Button(window, text="Ver el plan de ejecución real simple", font="Arial, 12", command = lambda:showPlain(connection, T.get("1.0","end"), "analyze true"))
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
