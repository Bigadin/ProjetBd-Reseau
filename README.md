# Documentation du script `server.py`

## Objectif
Ce script représente le serveur principal qui gère les communications avec les clients selon un protocole spécifique. Il valide les requêtes dans un ordre défini et répond avec des informations basées sur les données disponibles et les traitements effectués.

---

## Fonctionnalités principales

### 1. **Démarrage du serveur**
- Le serveur est démarré sur l'adresse et le port spécifiés dans le fichier de configuration `Config.conf`.
- Il écoute les connexions entrantes des clients via TCP.
- Un journal des événements (`server.log`) est utilisé pour consigner les activités du serveur.

---

### 2. **Gestion des clients**
- Les clients doivent suivre un protocole défini dans l'ordre suivant :
  1. `R_BRI` : Vérification de la borne.
  2. `R_ST` : Vérification de la station.
  3. `R_CI` : Vérification de la carte.
  4. `R_DU` : Vérification de la dernière utilisation.
  5. `R_JI` : Journalisation des actions.
- Si un client ne suit pas cet ordre, une erreur est renvoyée avec le message : "Vous ne suivez pas le protocole".

---

### 3. **Traitement des requêtes**
- Les requêtes sont analysées pour en extraire des données clés (`requestType`, `requestId`, etc.).
- Les types de requêtes traités sont :
  - **`CONNECT`** : Le client établit une connexion avec le serveur.
  - **`DISCONNECT`** : Le client se déconnecte proprement.
  - **`R_BRI`** : Appelle la fonction `Check_borne` pour vérifier l'état de la borne et de la station associée.
  - **`R_ST`** : Appelle la fonction `Check_station` pour vérifier l'état d'une station.
  - **`R_CI`** : Appelle la fonction `Check_carte` pour valider les informations d'une carte.
  - **`R_DU`** : Appelle la fonction `Respond_LastUse` pour vérifier la dernière utilisation de la carte.
  - **`R_JI`** : Appelle la fonction `Update_data` pour enregistrer une action dans la base de données.
- Les réponses aux requêtes sont structurées et formatées via la fonction `format_response`.

---

### 4. **Vérification du protocole**
- Le protocole est suivi à l'aide de l'état actuel du client, stocké dans un dictionnaire `client_states`.
- À chaque requête, l'état du client est mis à jour pour avancer dans le protocole.
- Si l'ordre des requêtes n'est pas respecté, le serveur retourne une erreur avec :
  - `response_type:REIV`
  - `status_code:400`
  - `action_code:2433`
  - `message:Vous ne suivez pas le protocole`

---

### 5. **Gestion des erreurs**
- Les erreurs de traitement sont capturées et une réponse générique est envoyée au client avec :
  - `response_type:REIV`
  - `status_code:500`
  - `action_code:2433`
  - `message:Erreur du serveur`
- Les exceptions sont consignées dans le journal d'erreurs.

---

### 6. **Structure des réponses**
Les réponses envoyées au client contiennent les informations suivantes :
- **`response_type`** : Type de réponse (`REV` pour succès, `REIV` pour erreur).
- **`status_code`** : Code de statut (exemple : `100` pour succès, `400` pour erreur client).
- **`action_code`** : Code indiquant l'action à réaliser.
- **`message`** : Message explicatif.
- **`timestamp`** : Horodatage de la réponse.

---

## Dépendances
- **`Cheching.py`** :
  - Fournit les fonctions pour vérifier les données des cartes, bornes et stations, ainsi que pour gérer les actions.
- **`BDD_Server_connection.py`** :
  - Gère la connexion à la base de données PostgreSQL.
  - Effectue les requêtes SQL nécessaires pour récupérer et mettre à jour les données.
- **Fichier de configuration `Config.conf`** :
  - Contient les paramètres de connexion du serveur (`host`, `port`).

---

## Données manipulées
- **Requêtes client** : Reçoivent des identifiants (ID de borne, ID de carte, ID de station) et des paramètres (date d'expiration).
- **Base de données** : Les informations sur les bornes, cartes, stations et journaux d'utilisation sont récupérées ou mises à jour.
- **Protocole** : L'ordre des étapes est strictement respecté pour chaque client.

---


# Documentation du script de vérifications (`Cheching.py`)

## Objectif
Ce script regroupe toutes les fonctions de validation et de vérification nécessaires pour le traitement des requêtes envoyées par les clients. Il s'appuie sur la base de données pour récupérer les informations nécessaires et produire des réponses adaptées au protocole défini.

---

## Fonctionnalités principales

### 1. **Classe `Response`**
- Définit le format standard des réponses renvoyées au client.
- Contient les informations suivantes :
  - `response_type` : Type de réponse (`REV` pour succès, `REIV` pour erreur).
  - `status_code` : Code de statut (exemple : `100` pour succès, `500` pour erreur serveur).
  - `action_code` : Code d'action pour guider le comportement client.
  - `message` : Message explicatif.
  - `timestamp` : Horodatage de la réponse.

---

### 2. **Validation de la carte (`Check_carte`)**
- Vérifie plusieurs conditions liées à une carte :
  1. **Existence** : La carte existe-t-elle dans la base de données (`existe_carte`) ?
  2. **Dernière utilisation** : La carte a-t-elle été utilisée récemment (`check_Last_Use`) ?
  3. **Date d'expiration** : La carte est-elle encore valide (`check_date`) ?
- Retourne une réponse appropriée en fonction de ces conditions.

---

### 3. **Validation de la station (`Check_station`)**
- Vérifie si une station existe et si elle est ouverte.
- Retourne :
  - Succès (`REV`) si la station est ouverte.
  - Erreur (`REIV`) si la station est fermée ou inexistante.

---

### 4. **Validation de la borne (`Check_borne`)**
- Vérifie plusieurs aspects d'une borne :
  1. Existence de la borne (`etat_borne`).
  2. Existence de la station associée à la borne (`etat_station`).
  3. Statut de la borne (ouverte, en panne, ou autre).
- Retourne une réponse détaillée selon ces vérifications.

---

### 5. **Récupération des données depuis la base**
- **`getAdherentFromCarte`** : Récupère l'identifiant de l'adhérent lié à une carte.
- **`getStationFromBorne`** : Récupère l'identifiant de la station associée à une borne.

---

### 6. **Gestion des badging**
- **`addBadgingToBD`** :
  - Ajoute une opération de badging dans la base de données.
  - Vérifie que les identifiants fournis (`id_adherent` et `id_station`) sont conformes (chaînes de 10 caractères).
  - Retourne :
    - `0` si l'enregistrement a réussi.
    - `1` si une erreur s'est produite.
- **`Update_data`** :
  - Met à jour les données après une validation réussie.
  - Associe un adhérent à une station via une borne.

---

### 7. **Dernière utilisation de la carte**
- **`check_Last_Use`** :
  - Vérifie la dernière utilisation d'une carte.
  - Retourne :
    - `0` si plus de 2 minutes se sont écoulées depuis la dernière utilisation.
    - `2` si moins de 2 minutes se sont écoulées.
    - `1` si aucune utilisation récente n'est trouvée.
- **`Respond_LastUse`** :
  - Génère une réponse basée sur `check_Last_Use`.
  - Messages possibles :
    - "Carte validée il y a plus de 2 minutes" (`REV`).
    - "Vous venez de valider, vous ne pouvez pas revalider" (`REIV`).
    - "Aucune validation récente trouvée pour cette carte" (`REIV`).

---

## Dépendances
- **`BDD_Server_connection.py`** :
  - Fournit les fonctions pour interagir avec la base de données PostgreSQL :
    - `getFromQuery` : Exécute une requête SQL et retourne plusieurs résultats.
    - `getFirstFromQuery` : Exécute une requête SQL et retourne un seul résultat.
    - `InsertInDataBase` : Insère des données dans la base et valide la transaction.
- **`codes.py`** :
  - Contient les codes de succès et d'erreurs utilisés dans les réponses :
    - `success_codes`
    - `server_error_codes`
    - `client_error_codes`
    - `borne_error_codes`

---

## Données manipulées
- **Cartes** :
  - Validation des informations (existence, date d'expiration, dernière utilisation).
  - Association avec un adhérent via la table `carte`.
- **Bornes** :
  - Validation de leur statut (ouverte, en panne, etc.).
  - Vérification de leur association avec une station.
- **Stations** :
  - Validation de leur statut (ouverte, fermée, en travaux).
- **Badging** :
  - Enregistrement des interactions dans la table `badger` :
    - `id_adherent`
    - `id_station`
    - `date_heure`

---

## Gestion des erreurs
- Chaque fonction gère ses erreurs via des blocs `try/except`.
- Les erreurs SQL déclenchent un rollback pour éviter des transactions incomplètes.
- Les réponses en cas d'erreurs incluent :
  - Type de réponse : `REIV`
  - Code de statut : `500` (erreur serveur)
  - Code d'action : `2433`
  - Message détaillé décrivant l'erreur
---

## Exemple d'utilisation des fonctions

### 1. Validation de la carte
Cette fonction valide l'existence d'une carte, sa date d'expiration, et vérifie son dernier usage.

```
response = Check_carte("1234567890", datetime.strptime("2025-12-15", "%Y-%m-%d"))
print(response.message)
```


### 2. Validation d'une borne
Cette fonction vérifie si une borne est en état de fonctionnement et si elle est associée à une station ouverte. 

```
response = Check_borne("Borne1234", "Station5678")
print(response.message)
```
### 3. Ajout de badging
Cette fonction enregistre dans la base de données une interaction entre un adhérent et une station via une borne.

```
result = addBadgingToBD("1234567890", "Station5678")
print("Badging réussi" if result == 0 else "Erreur lors du badging")
```


# Description programme Client

Ce programme est un client Java qui interagit avec un serveur pour effectuer une série de vérifications liées à une borne, une station, une carte, et la dernière utilisation d'une carte. Le programme utilise un fichier de configuration pour récupérer les paramètres nécessaires et gère les étapes de connexion, requêtes, et déconnexion avec le serveur. 

## Fonctionnalités

1. **Chargement de la configuration :** 
   - Le fichier `config.properties` est utilisé pour configurer l'hôte, le port, l'identifiant de la borne (`id_current_borne`) et de la station (`id_current_station`).

2. **Interaction avec l'utilisateur :**
   - Le programme demande à l'utilisateur d'entrer l'identifiant de la carte (`id_carte`) et la date d'expiration (`date_ex`).

3. **Communication avec le serveur :**
   - Le programme s'appuie sur la classe `Message` pour envoyer des requêtes au serveur via des appels à des méthodes spécifiques.

4. **Gestion des réponses du serveur :**
   - Le programme analyse les réponses reçues et exécute des actions spécifiques en fonction du `action_code` contenu dans la réponse.

5. **Gestion de la déconnexion :**
   - Si une action nécessite d'interrompre le processus (ex. : fermeture ou blocage de la borne), le client se déconnecte automatiquement du serveur.

---

## Structure

### Étapes principales du programme

1. **Chargement du fichier de configuration :**
   - Le fichier `config.properties` est chargé pour récupérer les valeurs nécessaires, comme l'hôte, le port, et les identifiants de la borne/station.

2. **Connexion au serveur :**
   - La méthode `connect()` de la classe `Message` est utilisée pour établir une connexion avec le serveur.

3. **Envoi des requêtes :**
   - Le programme envoie les requêtes suivantes dans cet ordre :
     - `Requet_GetBorne` : Vérifie l'état de la borne.
     - `Requet_GetStation` : Vérifie l'état de la station.
     - `Requet_GetCarte` : Vérifie la validité de la carte.
     - `Requet_GETDU` : Vérifie la dernière utilisation de la carte.

4. **Traitement des réponses :**
   - La méthode `handleResponse()` analyse les réponses et exécute des actions spécifiques en fonction du code d'action (`action_code`).

5. **Déconnexion :**
   - La méthode `disconnect()` est appelée à la fin du processus ou en cas d'action nécessitant l'arrêt (ex. : fermeture ou blocage).

---

## Dépendance

### `Message.java`

Le programme dépend de la classe `Message` qui gère les opérations suivantes :

1. **Connexion et déconnexion avec le serveur :**
   - `connect(String host, int port)` : Établit la connexion avec le serveur.
   - `disconnect()` : Déconnecte proprement le client du serveur.

2. **Envoi des requêtes :**
   - Méthodes pour envoyer des requêtes spécifiques :
     - `Requet_GetBorne(String id_borne, String id_station)`
     - `Requet_GetStation(String id_station)`
     - `Requet_GetCarte(String id_carte, String date_exp)`
     - `Requet_GETDU(String id_carte)`
     - `Requet_Journalisation(String id_carte, String id_borne)`

3. **Gestion des réponses :**
   - Chaque méthode de requête retourne la réponse reçue du serveur, qui est ensuite analysée dans la méthode `handleResponse()` du programme principal.

4. **Journalisation des requêtes et réponses :**
   - La classe `Message` inclut une fonctionnalité de journalisation pour enregistrer les requêtes et les réponses dans un fichier log.

---

## Fichier de configuration

Le fichier `config.properties` doit contenir les informations suivantes :

```properties
host=localhost
port=4546
id_current_borne=BN00000001
id_current_station=ST00000001
```

---
## Comment exécuter

1. Assurez-vous que le fichier `config.properties` est présent dans le même répertoire que le programme.
2. Compilez et exécutez le programme :
   ```bash
   javac Client.java
   java Client
   ```
Suivez les instructions pour entrer l'ID de la carte et la date d'expiration.
Observez les résultats des vérifications et les actions exécutées.
Avertissement
Ce programme nécessite la classe Message.java pour fonctionner.
Assurez-vous que le serveur est en cours d'exécution avant de lancer le programme.