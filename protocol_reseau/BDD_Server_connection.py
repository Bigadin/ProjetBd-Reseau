import psycopg2

# Fonction pour lire le fichier de configuration
def read_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Ignorer les lignes vides et les commentaires
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Diviser la ligne en clé et valeur
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
    return config

# Lecture de la configuration depuis le fichier
config = read_config(r"protocol_reseau\Config.conf")

# Récupération des paramètres de connexion à partir du fichier de configuration
bdhost = config.get("bdhost")
database = config.get("database")
user = config.get("user")
password = config.get("password")
port = config.get("bdport")

print(bdhost, database, user, password, port)

# Connexion et exécution de la requête
try:
    # Établir la connexion à la base de données PostgreSQL
    conn = psycopg2.connect(
        host=bdhost,
        database=database,
        user=user,
        password=password,
        port=port
    )
    print("Connexion réussie à la base de données")

    # Créer un curseur pour exécuter des requêtes SQL
    with conn.cursor() as cursor:
        # Exemple de requête : récupérer la version PostgreSQL
        cursor.execute("SELECT version()")
        # Afficher le résultat de la requête
        version = cursor.fetchall()
        print(f"Version : {version[0]}")

except Exception as e:
    # Gestion des erreurs de connexion ou de requête
    print(f"Erreur lors de la connexion ou de l'exécution de la requête : {e}")

# Fonction pour exécuter une requête et retourner tous les résultats
def getFromQuery(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {query}")
        print(f"Détail de l'erreur : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return None

# Fonction pour exécuter une requête et retourner uniquement le premier résultat
def getFirstFromQuery(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {query}")
        print(f"Détail de l'erreur : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return None

# Fonction pour insérer des données dans la base et valider la transaction
def InsertInDataBase(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()  # Valider la transaction si tout s'est bien passé
            return cursor
    except Exception as e:
        print(f"Erreur lors de l'insertion : {query}")
        print(f"Détail de l'erreur : {e}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
        return None

# Fonction pour fermer la connexion à la base de données
def closeCnx():
    conn.close()
    print("Connexion à la base de données fermée")
