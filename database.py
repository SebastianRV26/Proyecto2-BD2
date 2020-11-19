import psycopg2


class Database:
    """"
    Class for the database connection
    """

    connection = None  # db connection
    globalUser = ""  # name of the user using the db

    @staticmethod
    def createConnection(user, password, server, port, db):
        """"
        Creates the connection with the database using the specified credentials.
        """
        Database.globalUser = user
        try:
            Database.connection = psycopg2.connect(user=user,
                                                   password=password,
                                                   host=server,
                                                   port=port,
                                                   database=db)
            return Database.connection
        except (Exception, psycopg2.Error) as error:
            print("Error conectando a PostgreSQL", error)
            return None
