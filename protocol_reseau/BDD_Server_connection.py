import psycopg2

# Paramètres de connexion
host = "localhost"            # Adresse du serveur (ex : "localhost" pour une connexion locale)
database = "TransportDB"     # Nom de la base de données à laquelle se connecter
user = "postgres"       # Nom de l'utilisateur PostgreSQL
password = "4252"      # Mot de passe de cet utilisateur

# Connexion et exécution de la requête
try:
    # Établir la connexion
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes
    with conn.cursor() as cursor:
        # Requête de test : obtenir la version de PostgreSQL
        cursor.execute("SELECT version()")
        # Récupérer et afficher le résultat de la requête
        version = cursor.fetchall()
        print(f"version : {version[0]}")

except Exception as e:
    print(f"Erreur lors de la connexion ou de la requête : {e}")



def getFromQuery(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def getFirstFromQuery(query):
    with conn.cursor() as cursorF:
        cursorF.execute(query)
        return cursorF.fetchone()
    
def InsertInDataBase(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()
        return cursor
    
def closeCnx():
    conn.close()
