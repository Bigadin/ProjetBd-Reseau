package client_borne;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class Message {
	public Message() {
		
	}
	
	public  String Requet_Journalisation(String host ,int port, String id_carte, String id_borne) {
        String response = "";
        try (Socket socket = new Socket(host, port)) {
            String requestType = "R_JI";
            String requestId = "721";
            String borneID = id_borne; 
            String adherent = id_carte;

            String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_carte:" + adherent + "|id_borne:" + borneID + "|";


            OutputStream output = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(output, true);
            writer.println(request);
            System.out.println("Request sent: " + request);
            
            InputStream input = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
            response = reader.readLine();
            
            System.out.println("Server response: " + response);
          

	    } catch (UnknownHostException ex) {
	        System.out.println("Server not found: " + ex.getMessage());
	    } catch (IOException ex) {
	        System.out.println("I/O error: " + ex.getMessage());
	    }
        return response;
	}
	
	
	public  String Requet_GetCarte(String host ,int port, String id_carte, String _date_exp) {
        String response = "";
		 try (Socket socket = new Socket(host, port)) {
	            String requestType = "R_CI";
	            String requestId = "1031";
	            String date_exp = _date_exp; 
	            String adherent = id_carte;

	            String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_carte:" + adherent + "|date_exp:" + date_exp ;


	            OutputStream output = socket.getOutputStream();
	            PrintWriter writer = new PrintWriter(output, true);
	            writer.println(request);
	            System.out.println("Request sent: " + request);
	            
	            InputStream input = socket.getInputStream();
	            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
	            response = reader.readLine();
	            
	            System.out.println("Server response: " + response);

		    } catch (UnknownHostException ex) {
		        System.out.println("Server not found: " + ex.getMessage());
		    } catch (IOException ex) {
		        System.out.println("I/O error: " + ex.getMessage());
		    }
         return response;

	}
	
	public  String Requet_GetBorne(String host ,int port, String id_borne, String id_station) {
		String response = "";
		 try (Socket socket = new Socket(host, port)) {
	            String requestType = "R_BRI";
	            String requestId = "1001";
	            String borneID = id_borne; 
	            String stationID = id_station;

	            String request = "requestType:" + requestType + "|requestId:" + requestId + "|id_borne:"+ borneID + "|id_station:" + stationID + "|";


	            OutputStream output = socket.getOutputStream();
	            PrintWriter writer = new PrintWriter(output, true);
	            writer.println(request);
	            System.out.println("Request sent: " + request);
	            
	            InputStream input = socket.getInputStream();
	            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
	            response = reader.readLine();
	            
	            System.out.println("Server response: " + response);

		    } catch (UnknownHostException ex) {
		        System.out.println("Server not found: " + ex.getMessage());
		    } catch (IOException ex) {
		        System.out.println("I/O error: " + ex.getMessage());
		    }
         return response;

	}
}
