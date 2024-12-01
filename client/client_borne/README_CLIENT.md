# README

## Description

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