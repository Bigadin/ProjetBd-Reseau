import socket
from datetime import datetime, timedelta
import time
from codes import success_codes,server_error_codes,client_error_codes,borne_error_codes
from BDD_Server_connection import getFromQuery, getFirstFromQuery ,InsertInDataBase

class Response:
    def __init__(self, response_type, status_code, action_code, message,timestamp):
        self.response_type = response_type
        self.status_code = status_code
        self.action_code = action_code
        self.message = message
        self.timestamp = timestamp


timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def existe_carte(carteId):   #1 for not found   0 for found     3 for other
    query = f"SELECT * FROM carte WHERE numero = '{carteId}';"
    result =  getFromQuery(query)
    if not result:
        print(f"{result}")
        return 1
    else:
        return 0

def etat_borne(id_borne):
    query = f"SELECT statut FROM borne WHERE id_borne = '{id_borne}';"
    result =  getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result
    
def etat_station(id_station):
    query = f"SELECT statut FROM station WHERE id_station = '{id_station}';"
    result =  getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result
    
    
def check_date(ex_date):
    if(ex_date > datetime.today()):
        return True
    else :
        return False

    
def Check_carte(body,exdate):   
     
    IsExisteCarte = existe_carte(body)
    if(IsExisteCarte == 0):
        if(check_date(exdate)):
            response_type = 'REV'
            status_code = '100'  
            action_code = '2333'  
            message = success_codes[int(status_code)]
        else :
            response_type = 'REIV'
            status_code = '203'
            action_code = '2433'
            message = client_error_codes[(int)(status_code)]  
    else:
        response_type = 'REIV'
        status_code = '204'  
        action_code = '2433'  
        message = client_error_codes[(int)(status_code)]    
    response = Response(response_type,status_code,action_code,message,timestamp)
    return response


def Check_station(body):
    return

def Check_borne(id_borne,id_station):
    if etat_borne(id_borne) == 1:
        return print("borne n'existe pas")
    if etat_station(id_station) == 1:
        return print("Station n'existe pas")
    borne = etat_borne(id_borne)[0]
    station = etat_station(id_station)[0]

    #verifier si la station est dans le statut ouvert(en fonctionnement)
    if(station == 'Ouverte'):
        print("Station ouverte \n")
        
        if borne == 'Ouverte': # en fonctionnement et non pas Ouverte
            print("Borne en fontionnement")
            response_type = 'REV'
            status_code = '100'  
            action_code = '2533'  
            message = success_codes[int(status_code)]
        elif borne == 'En panne':
            print("Borne en panne")
            response_type = 'REIV'
            status_code = '403'  
            action_code = '2633'  
            message = borne_error_codes[int(status_code)]
        elif borne == 1:
            print("Borne n'existe pas")
            response_type = 'REIV'
            status_code = '401'  
            action_code = '00'  
            message = borne_error_codes[int(status_code)]
        else:
            print("Borne ne fonctionne pas")
            response_type = 'REIV'
            status_code = '404'  
            action_code = '2633'  
            message = borne_error_codes[int(status_code)]
            
        
        
    else:
        print("Station fermée")
        response_type = 'REIV'
        status_code = '405'  
        action_code = '2633'  
        message = borne_error_codes[int(status_code)]
        
    reponse = Response(response_type,status_code,action_code,message,timestamp)
    return reponse


def getAdherentFromCarte(id_carte):
    query = f"SELECT adherent.id_adherent FROM carte JOIN adherent ON  adherent.id_adherent = carte.id_adherent AND carte.numero = '{id_carte}';"
    result =  getFirstFromQuery(query)
    if not result:
        return 1
    else:
        return result
def getStationFromBorne(id_borne):
    query = f"SELECT station.id_station FROM borne JOIN station ON  station.id_station = borne.id_station AND borne.id_borne = '{id_borne}';"
    result = getFirstFromQuery(query)
    print(result,query)
    if not result:
        return 1
    else:
        return result
    

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

        result = InsertInDataBase(query)
        print(f"Insert Result: {result.rowcount}")  # Log the row count

        if result.rowcount == 1:
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Error occurred: {e}")
        return 1



def Update_data(id_carte, id_borne):
    # ici on sait que la borne marche bien et que la carte est valide,
    # cette fonction sera appeler après l'ouverture des portes afin d'avoir les informations dans la base de données

    response_type = 'REIV'  # Default value
    status_code = '405'     # Default error status code
    action_code = '2633'    # Default action code for failure
    message = 'Une erreur inconnue est survenue'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp

    ade = getAdherentFromCarte(id_carte=id_carte)
    bst = getStationFromBorne(id_borne)

    if ade == 1:
        # Pas d'adhérent lié à cette carte, problème dans la base de données
        message = 'Pas d\'adhérent lié à cette carte!'
        return Response(response_type, status_code, action_code, message, timestamp)

    if bst == 1:
        # La borne n'est pas liée à une station
        message = 'La borne n\'est pas liée à une station!'
        return Response(response_type, status_code, action_code, message, timestamp)

    id_adherent = ade[0]
    id_station = bst[0]

    try:
        # Insérer dans la base de données l'information que cet adhérent a pris cette borne
        rep = addBadgingToBD(id_adherent, id_station)
        if rep == 1:
            # Erreur d'enregistrement
            message = 'Erreur d\'enregistrement dans la base de données'
        else:
            # Succès d'enregistrement
            response_type = 'REV'
            status_code = '100'
            action_code = '000'
            message = 'Enregistrement réussi!'
    except Exception as e:
        # Erreur inattendue lors de l'insertion
        message = f'Erreur lors de l\'insertion : {e}'

    # Crée et retourne la réponse
    return Response(response_type, status_code, action_code, message, timestamp)


            
        
