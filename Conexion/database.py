import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ANDY;"
            "DATABASE=pegratriplexsas;"
            "Trusted_Connection=yes;"
        )
        return conn

    except pyodbc.Error as e:
        print("Error al conectar con SQL Server")
        print(e)
        return None