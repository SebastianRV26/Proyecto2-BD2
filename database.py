import psycopg2

class Database:
    connection = None
    globalUser = ""

    @staticmethod
    def createConnection(user, password, server, port, db):
        """"
        Creates the connection with the database
        """
        Database.globalUser = "basesII"  # delete later
        try:
            # TODO: Está quemado, cambiarlo por los parametros
            Database.connection = psycopg2.connect(user="basesII",
                                    password="12345",
                                    host="leoviquez.com",
                                    port="5432",
                                    database="basesII")
            return Database.connection
        except (Exception, psycopg2.Error) as error:
            print("Error conectando a PostgreSQL", error)
            return None