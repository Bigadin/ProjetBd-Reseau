import psycopg2
from datetime import datetime

# Function to insert badge data
def addBadgingToBD(id_adherent, id_station):
    try:
        # Get the current timestamp and format it
        currentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).strip()

        # Construct the SQL query
        query = f"""
        INSERT INTO badge(id_adherent, id_station, dateheurs) 
        VALUES ('{id_adherent}', '{id_station}', '{currentTime}');
        """

        # Print the query for debugging purposes
        print(f"Generated Query: {query}")

        # Database connection parameters
        conn = psycopg2.connect(
            host = "localhost"    ,        # Adresse du serveur (ex : "localhost" pour une connexion locale)
            database = "TransportDB" ,    # Nom de la base de données à laquelle se connecter
            user = "postgres"   ,    # Nom de l'utilisateur PostgreSQL
            password = "4252" 
        )
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)

        # Commit the transaction
        conn.commit()

        # Check if one row was inserted
        if cursor.rowcount == 1:
            print("Insert successful!")
            return 0
        else:
            print("Insert failed!")
            return 1

    except Exception as e:
        # If an error occurs, print it and return 1
        print(f"Error occurred: {e}")
        return 1

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

# Example usage
id_adherent = 'AD00000002'
id_station = 'ST00000001'
result = addBadgingToBD(id_adherent, id_station)
print(f"Result code: {result}")
