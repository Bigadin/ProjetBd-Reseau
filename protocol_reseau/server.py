import socket
from datetime import datetime
import logging

from Cheching import Check_carte, Check_borne, Update_data, Check_station, Respond_LastUse
from BDD_Server_connection import read_config

# Lire le fichier de configuration
config = read_config(r"protocol_reseau\Config.conf")
HOST = config.get("host")
PORT = int(config.get("port", 0))

print(HOST, PORT)
isConnected = False

# Configurer le système de journalisation
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Ordre du protocole
PROTOCOL_SEQUENCE = ['R_BRI', 'R_ST', 'R_CI', 'R_DU', 'R_JI']

# Dictionnaire pour suivre l'état du protocole de chaque client
client_states = {}

def parse_message(data):
    try:
        # Diviser les champs et analyser les paires clé-valeur
        fields = data.split('|')
        parsed_data = {key_value.split(':')[0]: key_value.split(':')[1] for key_value in fields if ':' in key_value}
        return parsed_data
    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse du message : {str(e)}")

def handle_request(data, client_address):
    global isConnected
    
    # Initialiser l'état du protocole du client s'il n'est pas encore suivi
    if client_address not in client_states:
        client_states[client_address] = 0  # Commence par la première étape du protocole
    try:
        # Analyser la requête entrante
        parsed_data = parse_message(data)

        # Extraire les valeurs
        type_req = parsed_data.get("requestType", "")
        request_id = parsed_data.get("requestId", "")
        current_protocol_step = client_states[client_address]

        if data.strip() == "CONNECT":
            isConnected = True
            return "CONNECTED"
        elif data.strip() == "DISCONNECT":
            isConnected = False
            return "DISCONNECTED"

        if isConnected:
            print(current_protocol_step)

            # Vérifier que le protocole est respecté
            if current_protocol_step >= len(PROTOCOL_SEQUENCE) or type_req != PROTOCOL_SEQUENCE[current_protocol_step]:
                return f"response_type:REIV | status_code:400 | action_code:2433 | message:Vous ne suivez pas le protocole | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Traiter la requête actuelle et avancer à l'étape suivante
            if type_req == 'R_BRI' and request_id == '1001':
                id_borne = parsed_data.get("id_borne", "").strip()
                id_station = parsed_data.get("id_station", "").strip()
                response = Check_borne(id_borne, id_station)
                client_states[client_address] += 1  # Passer à l'étape suivante
                return format_response(response)

            elif type_req == 'R_ST' and request_id == '1021':
                id_station = parsed_data.get("id_station", "").strip()
                response = Check_station(id_station)
                client_states[client_address] += 1  # Passer à l'étape suivante
                return format_response(response)

            elif type_req == 'R_CI' and request_id == '1031':
                id_carte = parsed_data.get("id_carte", "").strip()
                date_ex = parsed_data.get("date_exp", "").strip()
                date_exp = datetime.strptime(date_ex, "%Y-%m-%d")
                response = Check_carte(id_carte, date_exp)
                client_states[client_address] += 1  # Passer à l'étape suivante
                return format_response(response)

            elif type_req == 'R_DU' and request_id == '1041':
                id_carte = parsed_data.get("id_carte", "").strip()
                response = Respond_LastUse(id_carte)
                client_states[client_address] += 1  # Passer à l'étape suivante
                return format_response(response)

            elif type_req == 'R_JI' and request_id == '721':
                id_borne = parsed_data.get("id_borne", "").strip()
                id_carte = parsed_data.get("id_carte", "").strip()
                response = Update_data(id_carte, id_borne)
                client_states.pop(client_address, None)  # Fin du protocole, réinitialiser l'état
                return format_response(response)

            else:
                return f"response_type:REIV | status_code:400 | action_code:2433 | message:Requête malformée | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        else:
            return f"response_type:REIV | status_code:403 | action_code:2433 | message:Aucune connexion détectée | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    except Exception as e:
        return f"response_type:REIV | status_code:500 | action_code:2433 | message:Erreur du serveur : {str(e)} | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def format_response(response):
    """Formate l'objet réponse en une chaîne de caractères."""
    return (
        f"response_type:{response.response_type} | "
        f"status_code:{response.status_code} | "
        f"action_code:{response.action_code} | "
        f"message:{response.message} | "
        f"timestamp:{response.timestamp}"
    )

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Serveur à l\'écoute sur {HOST}:{PORT}...')
        logging.info(f"Serveur démarré sur {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            logging.info(f"Connexion établie avec {addr}")
            print(f"Connecté par {addr}")
            conn.settimeout(20)  # Définir un délai d'attente de 20 secondes

            try:
                while True:
                    data = conn.recv(1024).decode()  # Recevoir une requête du client
                    if not data:  # Gérer la déconnexion du client
                        logging.info(f"Client {addr} déconnecté.")
                        print(f"Client {addr} déconnecté.")
                        break

                    logging.info(f"Requête reçue de {addr} : {data}")
                    print(f"Requête reçue : {data}")

                    # Traiter la requête
                    response = handle_request(data, addr)

                    response = f"{response}\n"  # Ajouter un saut de ligne
                    conn.sendall(response.encode("utf-8"))  # Envoyer la réponse
                    logging.info(f"Réponse envoyée à {addr} : {response}")
                    print(f"Réponse envoyée : {response}")

            except Exception as e:
                logging.error(f"Erreur lors du traitement du client {addr} : {e}")
                print(f"Erreur lors du traitement du client {addr} : {e}")
            finally:
                conn.close()
                logging.info(f"Connexion avec {addr} fermée.")
                print(f"Connexion avec {addr} fermée.")

if __name__ == '__main__':
    run_server()
