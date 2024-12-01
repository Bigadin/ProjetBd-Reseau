package client_borne;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.net.*;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {
        Properties config = new Properties();

        // Charger le fichier de configuration
        try (FileInputStream input = new FileInputStream("config.properties")) {
            config.load(input);
        } catch (IOException e) {
            System.err.println("Échec du chargement de la configuration : " + e.getMessage());
            return;
        }

        // Récupérer les valeurs de configuration
        String host = config.getProperty("host");
        int port = Integer.parseInt(config.getProperty("port"));
        String id_current_borne = config.getProperty("id_current_borne");
        String id_current_station = config.getProperty("id_current_station");

        System.out.println("Hôte : " + host);
        System.out.println("Port : " + port);
        System.out.println("ID Borne : " + id_current_borne);
        System.out.println("ID Station : " + id_current_station);
        
        Scanner scanner = new Scanner(System.in);

        // Demander à l'utilisateur de saisir l'ID de la carte
        System.out.print("Entrez l'ID de la carte (id_carte) : ");
        String id_carte = scanner.nextLine();

        // Demander à l'utilisateur de saisir la date d'expiration
        System.out.print("Entrez la date d'expiration (date_ex) au format AAAA-MM-JJ : ");
        String date_ex = scanner.nextLine();
        Message Mes = new Message();

        try {
            // Étape 1 : Connexion
            if (!Mes.connect(host, port)) {
                System.out.println("Échec de la connexion au serveur. Fin du processus...");
                return;
            }

            // Effectuer les requêtes
            System.out.println("Vérification de la borne...");
            String response = Mes.Requet_GetBorne(id_current_borne, id_current_station);
            if (!handleResponse(response, Mes, host, port, id_carte, id_current_borne)) return;

            System.out.println("Vérification de la station...");
            response = Mes.Requet_GetStation(id_current_station);
            if (!handleResponse(response, Mes, host, port, id_carte, id_current_borne)) return;

            System.out.println("Vérification de la carte...");
            response = Mes.Requet_GetCarte(id_carte, date_ex);
            if (!handleResponse(response, Mes, host, port, id_carte, id_current_borne)) return;

            System.out.println("Vérification de la dernière utilisation...");
            response = Mes.Requet_GETDU(id_carte);
            if (!handleResponse(response, Mes, host, port, id_carte, id_current_borne)) return;

            // Phase de déconnexion
            if (Mes.disconnect()) {
                System.out.println("Déconnexion réussie.");
            } else {
                System.out.println("Échec de la déconnexion.");
            }
        } catch (Exception e) {
            System.out.println("Une erreur est survenue : " + e.getMessage());
        }
    }

    // Méthode pour gérer la réponse du serveur et effectuer des actions
    private static boolean handleResponse(String response, Message Mes, String host, int port, String id_carte, String id_current_borne) {
        if (response == null || response.isEmpty()) {
            System.out.println("Aucune réponse reçue du serveur.");
            return false; // Arrêter le processus si la réponse est vide
        }

        // Analyser la réponse
        Map<String, String> responseMap = new HashMap<>();
        String[] parts = response.split("\\|");
        for (String part : parts) {
            String[] keyValue = part.split(":");
            if (keyValue.length == 2) {
                responseMap.put(keyValue[0].trim(), keyValue[1].trim());
            }
        }
        // Récupérer les valeurs spécifiques de la réponse
        String actionCode = responseMap.get("action_code");

        if (actionCode != null) {
            switch (actionCode) {
                case "2333":
                    System.out.println("Action : continuer");
                    break;
                case "2433":
                    System.out.println("Action : Bloquer la porte. Arrêt du processus.");
                    Mes.disconnect();
                    return false; // Arrêter le traitement
                case "2533":
                    System.out.println("Action : Ouvrir la borne");
                    break;
                case "2633":
                    System.out.println("Action : Fermer la borne. Arrêt du processus.");
                    Mes.disconnect();
                    return false; // Arrêter le traitement
                case "2733":
                    System.out.println("Action : Ouvrir la porte.");
                    Mes.Requet_Journalisation(id_carte, id_current_borne);
                    break;
                default:
                    System.out.println("Code d'action inconnu reçu : " + actionCode);
                    break;
            }
        } else {
            System.out.println("Erreur : 'action_code' non trouvé dans la réponse.");
        }

        return true; // Continuer le traitement
    }
}
