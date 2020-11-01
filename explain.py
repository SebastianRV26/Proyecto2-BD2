import tkinter as tk
import os
import psycopg2
import json

root = tk.Tk()
root.title("Plan de ejecucion - PostgresSQL")
T = tk.Text(root, height=25, width=100)
T.pack()
T.insert(tk.END, """--Inserte aquí su código SQL para mostrar el plan de ejecución
--código de ejemplo:
select * from 
    optimizacion.catastro_municipal as c
    inner join
    optimizacion.patentes as p 
    on st_contains(c.geom,p.geom5367)
                """)

def verPlan():
    try:
        conn = psycopg2.connect(user = "basesII",
                                password = "12345",
                                host = "leoviquez.com",
                                port = "5432",
                                database = "basesII")
        cursor = conn.cursor()       
        consulta=T.get("1.0","end")
        cursor.execute("""explain (format JSON, verbose true) 
                            
                            """+consulta)
        result = cursor.fetchone()
    except (Exception, psycopg2.Error) as error :
        print ("Error conectando a PostgreSQL", error)
    file = open(r"explain.json","wt")

    file.write(json.dumps(result[0]))
    file.close()
    os.system("python3 json_viewer.py explain.json")

B = tk.Button(root, text ="Ver plan", command = verPlan)
B.pack()
tk.mainloop()