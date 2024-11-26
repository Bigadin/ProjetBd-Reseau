package client_borne;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.net.*;


public class Client {
	

	
    public static void main(String[] args) {
        String host = "localhost"; // Server IP address
        int port = 4546;          // Server port
        String id_current_borne = "BN00000001";   // l'id du client qui est la borne
        String id_current_station = "ST00000003";   // l'id de la station ou est le client

        String requestType = "R_CI";
        String requestId = "1031";
        String id_carte = "987654321"; 
        String date_ex = "15-12-2025" ;
        
        // ceci est uniquement pour le test
        Scanner scanner = new Scanner(System.in); // Create a Scanner object for user input
        System.out.println("1 : VERIFIER BORNE,  2: VERIFIER CARTE: ");
        
        // Read user input
        String userInput = scanner.nextLine();
            
        Message Mes = new Message();
        String response = "aa";
        if ("2".equals(userInput)) {
            response = Mes.Requet_GetCarte(host, port, id_carte, date_ex);
        } else if ("1".equals(userInput)) {
            response = Mes.Requet_GetBorne(host, port, id_current_borne, id_current_station);
        } else {
            System.out.println("Invalid input. Exiting...");
            return;
        }
         // fin de la partie test
        // Parse the response
        Map<String, String> responseMap = new HashMap<>();
        String[] parts = response.split("\\|");
        for (String part : parts) {
            String[] keyValue = part.split(":");
            if (keyValue.length == 2) {
                responseMap.put(keyValue[0].trim(), keyValue[1].trim());
            }
        }

        // Get specific values from the response
        String actionCode = responseMap.get("action_code");
        if (actionCode != null) {
            switch (actionCode) {
                case "2333":
                    System.out.println("Action: Open the door");
                    Mes.Requet_Journalisation(host, port, id_carte, id_current_borne);
                    break;
                case "2433":
                    System.out.println("Action: Block the door");
                    break;
                case "2533":
                    System.out.println("Action: Open the borne");
                    break;
                case "2633":
                    System.out.println("Action: Close the borne");
                    break;
                default:
                    System.out.println("Unknown action code received: " + actionCode);
                    break;
            }
        } else {
            System.out.println("Error: 'action_code' not found in response.");
        }

    }
}

//