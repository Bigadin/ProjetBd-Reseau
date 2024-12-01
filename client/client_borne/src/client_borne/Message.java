package client_borne;

import java.io.*;
import java.net.Socket;
import java.net.SocketTimeoutException;

public class Message {
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;

    // Constructeur
    public Message() {}

    // Se connecter au serveur
    public boolean connect(String host, int port) {
        try {
            socket = new Socket(host, port);
            socket.setSoTimeout(20000); // Définit un délai d'attente de 20 secondes
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));

            // Envoie la commande CONNECT au serveur
            out.println("CONNECT");
            String response = in.readLine();
            if (response != null && response.equals("CONNECTED")) {
                System.out.println("Connecté au serveur avec succès.");
                return true;
            } else {
                System.out.println("Réponse inattendue du serveur : " + response);
            }
        } catch (IOException e) {
            System.err.println("Échec de la connexion : " + e.getMessage());
        }
        return false;
    }

    // Se déconnecter du serveur
    public boolean disconnect() {
        try {
            // Envoie la commande DISCONNECT au serveur
            out.println("DISCONNECT");
            String response = in.readLine();
            if (response != null && response.equals("DISCONNECTED")) {
                System.out.println("Déconnecté du serveur avec succès.");
                closeConnection(); // Ferme les connexions
                return true;
            } else {
                System.out.println("Réponse inattendue du serveur : " + response);
            }
        } catch (IOException e) {
            System.err.println("Échec de la déconnexion : " + e.getMessage());
        }
        return false;
    }

    // Ferme toutes les connexions
    private void closeConnection() throws IOException {
        if (in != null) in.close();
        if (out != null) out.close();
        if (socket != null) socket.close();
    }

    // Envoie des requêtes via la connexion persistante
    public String sendRequest(String request) {
        String response = "";
        try {
            if (socket == null || socket.isClosed()) {
                System.out.println("Erreur : Pas de connexion active au serveur.");
                return null;
            }

            // Envoie la requête
            out.println(request);
            System.out.println("Requête envoyée : " + request);

            // Reçoit la réponse avec un délai d'attente de 20 secondes
            try {
                response = in.readLine();
                if (response != null) {
                    System.out.println("Réponse reçue : " + response);
                } else {
                    System.out.println("Aucune réponse reçue du serveur.");
                }
            } catch (SocketTimeoutException e) {
                System.out.println("Délai dépassé : Aucune réponse reçue dans les 20 secondes. Déconnexion...");
                disconnect(); // Déconnecte le client en cas de délai dépassé
                return null;
            }

            logRequestResponse(request, response); // Journalise la requête et la réponse

        } catch (IOException e) {
            System.err.println("Erreur pendant la communication : " + e.getMessage());
        }
        return response;
    }

    // Méthodes spécifiques pour envoyer des requêtes
    public String Requet_GetBorne(String id_borne, String id_station) {
        String requestType = "R_BRI";
        String requestId = "1001";
        String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_borne:" + id_borne + "|id_station:" + id_station + "|";
        return sendRequest(request);
    }

    public String Requet_GetStation(String id_station) {
        String requestType = "R_ST";
        String requestId = "1021";
        String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_station:" + id_station + "|";
        return sendRequest(request);
    }

    public String Requet_GetCarte(String id_carte, String date_exp) {
        String requestType = "R_CI";
        String requestId = "1031";
        String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_carte:" + id_carte + "|date_exp:" + date_exp + "|";
        return sendRequest(request);
    }

    public String Requet_GETDU(String id_carte) {
        String requestType = "R_DU";
        String requestId = "1041";
        String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_carte:" + id_carte + "|";
        return sendRequest(request);
    }

    public String Requet_Journalisation(String id_carte, String id_borne) {
        String requestType = "R_JI";
        String requestId = "721";
        String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_carte:" + id_carte + "|id_borne:" + id_borne + "|";
        return sendRequest(request);
    }

    // Journalise les requêtes et réponses dans un fichier
    public void logRequestResponse(String request, String response) {
        System.out.println("Journalisation de la requête et de la réponse...");

        // Journalise dans un fichier
        try (FileWriter logFile = new FileWriter("client_debug.log", true)) {
            logFile.write("Requête : " + request + "\n");
            logFile.write("Réponse : " + response + "\n");
            logFile.write("----------------------------------------\n");
        } catch (IOException e) {
            System.err.println("Échec de la journalisation de la requête et de la réponse : " + e.getMessage());
        }
    }
}
