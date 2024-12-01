import socket
from datetime import datetime, timedelta
import time
from codes import success_codes, server_error_codes, client_error_codes, borne_error_codes
from BDD_Server_connection import getFromQuery, getFirstFromQuery, InsertInDataBase

class Response:
    def __init__(self, response_type, status_code, action_code, message, timestamp):
        self.response_type = response_type
        self.status_code = status_code
        self.action_code = action_code
        self.message = message
        self.timestamp = timestamp

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Vérifie si la carte existe dans la base de données
# Retourne 0 si trouvée, 1 si non trouvée
def existe_carte(carteId):
    query = f"SELECT * FROM carte WHERE numero = '{carteId}';"
    result = getFromQuery(query)
    if not result:
        print(f"{result}")
        return 1
    else:
        return 0

# Récupère le statut d'une borne spécifique
# Retourne le statut ou 1 si la borne n'existe pas
def etat_borne(id_borne):
    query = f"SELECT statut FROM borne WHERE id_borne = '{id_borne}';"
    result = getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result

# Récupère le statut d'une station spécifique
# Retourne le statut ou 1 si la station n'existe pas
def etat_station(id_station):
    query = f"SELECT statut FROM station WHERE id_station = '{id_station}';"
    result = getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result

# Vérifie si la date d'expiration donnée est valide
# Retourne True si la date est dans le futur, False sinon
def check_date(ex_date):
    if ex_date > datetime.today():
        return True
    else:
        return False

# Valide l'existence, la date d'expiration et le dernier usage de la carte
def Check_carte(body, exdate):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Valeurs par défaut pour la réponse en cas d'erreurs inattendues
    response_type = 'REIV'
    status_code = '500'  # Erreur interne du serveur
    action_code = '2433'
    message = "Erreur inattendue."

    try:
        # Vérifie si la carte existe dans la base de données
        IsExisteCarte = existe_carte(body)
        if IsExisteCarte == 0:
            # Vérifie si le dernier usage de la carte est valide
            if check_Last_Use(body) == 0:
                # Vérifie la date d'expiration de la carte
                if check_date(exdate):
                    response_type = 'REV'
                    status_code = '100'
                    action_code = '2333'
                    message = success_codes[int(status_code)]
                else:
                    response_type = 'REIV'
                    status_code = '203'
                    action_code = '2433'
                    message = client_error_codes[int(status_code)]
            else:
                response_type = 'REIV'
                status_code = '205'
                action_code = '2433'
                message = client_error_codes[int(status_code)]
        else:
            response_type = 'REIV'
            status_code = '204'
            action_code = '2433'
            message = client_error_codes[int(status_code)]
    except Exception as e:
        # Gestion des erreurs inattendues
        response_type = 'REIV'
        status_code = '500'
        action_code = '2433'
        message = f"Erreur : {str(e)}"

    # Crée et retourne l'objet Response
    response = Response(response_type, status_code, action_code, message, timestamp)
    return response

# Vérifie si la station est ouverte ou fermée
def Check_station(id_station):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if etat_station(id_station) == 1:
        response_type = 'REIV'
        status_code = '405'
        action_code = '2633'
        message = "Station inexistante."
        return Response(response_type, status_code, action_code, message, timestamp)

    statut_ST = etat_station(id_station)[0]
    if statut_ST == 'Ouverte':
        print("La station est ouverte.")
        response_type = 'REV'
        status_code = '100'
        action_code = '2533'
        message = success_codes[int(status_code)] + " Station ouverte."
    if statut_ST in ('Fermé', 'Travaux'):
        print("La station est fermée.")
        response_type = 'REIV'
        status_code = '405'
        action_code = '2633'
        message = success_codes[int(status_code)]

    return Response(response_type, status_code, action_code, message, timestamp)

# Vérifie si la borne est en état de fonctionnement
def Check_borne(id_borne, id_station):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Vérifie si la borne et la station existent
        if etat_borne(id_borne) == 1:
            message = "La borne n'existe pas."
            print(message)
            return Response('REIV', '401', '2633', message, timestamp)

        if etat_station(id_station) == 1:
            message = "La station n'existe pas."
            print(message)
            return Response('REIV', '402', '2633', message, timestamp)

        # Récupère le statut de la borne et de la station
        borne = etat_borne(id_borne)[0]
        station = etat_station(id_station)[0]

        # Vérifie si la station est ouverte
        if station == 'Ouverte':
            print("Station ouverte.\n")

            if borne == 'Ouverte':  # Borne en état de fonctionnement
                print("Borne en fonctionnement.")
                response_type = 'REV'
                status_code = '100'
                action_code = '2533'
                message = success_codes[int(status_code)]
            elif borne == 'En panne':  # Borne hors service
                print("Borne en panne.")
                response_type = 'REIV'
                status_code = '403'
                action_code = '2633'
                message = borne_error_codes[int(status_code)]
            else:  # Autres états de la borne
                print("Borne hors service.")
                response_type = 'REIV'
                status_code = '404'
                action_code = '2633'
                message = borne_error_codes[int(status_code)]
        else:
            # La station est fermée
            print("Station fermée.")
            response_type = 'REIV'
            status_code = '405'
            action_code = '2633'
            message = borne_error_codes[int(status_code)]

    except Exception as e:
        # Gestion des erreurs inattendues
        print(f"Erreur inattendue : {e}")
        response_type = 'REIV'
        status_code = '500'
        action_code = '2433'
        message = f"Erreur : {str(e)}"

    return Response(response_type, status_code, action_code, message, timestamp)

# Récupère l'identifiant de l'adhérent à partir du numéro de carte
# Retourne 1 si aucun adhérent n'est trouvé
def getAdherentFromCarte(id_carte):
    query = f"SELECT adherent.id_adherent FROM carte JOIN adherent ON adherent.id_adherent = carte.id_adherent AND carte.numero = '{id_carte}';"
    result = getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result

# Récupère l'identifiant de la station associée à une borne
# Retourne 1 si aucune station n'est trouvée
def getStationFromBorne(id_borne):
    query = f"SELECT station.id_station FROM borne JOIN station ON station.id_station = borne.id_station AND borne.id_borne = '{id_borne}';"
    result = getFirstFromQuery(query)
    print(result, query)
    if not result:
        return 1
    else:
        return result

# Ajoute une opération de badging dans la base de données
# Vérifie également que les identifiants sont conformes (string de 10 caractères)
def addBadgingToBD(id_adherent, id_station):
    try:
        # Vérifie que les identifiants sont des chaînes de 10 caractères
        if not (isinstance(id_adherent, str) and isinstance(id_station, str)):
            print("Erreur : id_adherent et id_station doivent être des chaînes.")
            return 1

        if len(id_adherent) != 10 or len(id_station) != 10:
            print("Erreur : id_adherent et id_station doivent contenir exactement 10 caractères.")
            return 1

        # Récupère le timestamp actuel
        currentTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).strip()

        # Crée la requête SQL
        query = f"""
        INSERT INTO badger(id_adherent, id_station, date_heure) 
        VALUES ('{id_adherent}', '{id_station}', '{currentTime}');
        """

        # Affiche la requête pour le débogage
        print(f"Requête générée : {query}")

        result = InsertInDataBase(query)
        print(f"Résultat de l'insertion : {result.rowcount}")  # Affiche le nombre de lignes insérées

        if result.rowcount == 1:
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Erreur rencontrée : {e}")
        return 1

# Met à jour les données après une validation réussie
# Associe l'adhérent et la station liés à la borne
def Update_data(id_carte, id_borne):
    # Par défaut, réponse indiquant une erreur
    response_type = 'REIV'
    status_code = '405'
    action_code = '2633'
    message = 'Une erreur inconnue est survenue'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ade = getAdherentFromCarte(id_carte=id_carte)
    bst = getStationFromBorne(id_borne)

    if ade == 1:
        # Aucun adhérent associé à cette carte
        message = "Pas d'adhérent lié à cette carte !"
        return Response(response_type, status_code, action_code, message, timestamp)

    if bst == 1:
        # La borne n'est pas associée à une station
        message = "La borne n'est pas associée à une station !"
        return Response(response_type, status_code, action_code, message, timestamp)

    id_adherent = ade[0]
    id_station = bst[0]

    try:
        # Insère une opération de badging dans la base de données
        rep = addBadgingToBD(id_adherent, id_station)
        if rep == 1:
            # Erreur lors de l'enregistrement
            message = "Erreur d'enregistrement dans la base de données"
        else:
            # Enregistrement réussi
            response_type = 'REV'
            status_code = '100'
            action_code = '000'
            message = "Enregistrement réussi !"
    except Exception as e:
        # Gestion des erreurs inattendues
        message = f"Erreur lors de l'insertion : {e}"

    return Response(response_type, status_code, action_code, message, timestamp)

# Vérifie la dernière utilisation de la carte
# Retourne 0 si plus de 2 minutes se sont écoulées, 2 sinon
def check_Last_Use(id_carte):
    query = f"""
        SELECT date_heure FROM badger WHERE id_adherent = (
            SELECT id_adherent FROM carte WHERE numero = '{id_carte}'
        )
        ORDER BY date_heure DESC
        LIMIT 1;
    """
    result = getFirstFromQuery(query)
    print(result)
    if not result:
        return 0
    else:
        given_date = datetime.strptime(str(result[0]), "%Y-%m-%d %H:%M:%S")

        current_date = datetime.now()

        time_difference = current_date - given_date

        # Vérifie si la différence est inférieure à 2 minutes
        if time_difference < timedelta(minutes=2):
            return 2
        else:
            return 0

# Génère une réponse concernant la dernière utilisation de la carte
def Respond_LastUse(id_carte):
    last_use = check_Last_Use(id_carte)
    print(last_use)
    if last_use == 1:
        response_type = 'REIV'
        status_code = '404'
        action_code = '2434'
        message = "Aucune validation récente trouvée pour cette carte"
    elif last_use == 2:
        response_type = 'REIV'
        status_code = '405'
        action_code = '2433'
        message = "Vous venez de valider, vous ne pouvez pas revalider"
    elif last_use == 0:
        response_type = 'REV'
        status_code = '100'
        action_code = '2733'
        message = "Carte validée il y a plus de 2 minutes"
    else:
        response_type = 'REIV'
        status_code = '500'
        action_code = '2433'
        message = "Erreur inconnue"

    return Response(response_type, status_code, action_code, message, timestamp)
