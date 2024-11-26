import socket
from datetime import datetime, timedelta
import time
from Cheching import Check_carte,Check_borne,Update_data

# Define the response status codes and action codes



HOST = 'localhost'  
PORT = 4546


def parse_message(data):
    try:
        # Split fields and parse key-value pairs
        fields = data.split('|')
        parsed_data = {key_value.split(':')[0]: key_value.split(':')[1] for key_value in fields if ':' in key_value}
        return parsed_data
    except Exception as e:
        raise ValueError(f"Error parsing message: {str(e)}")

def handle_request(data):
    try:
        # Parse the incoming request
        parsed_data = parse_message(data)

        # Extract values
        type_req = parsed_data.get("requestType", "")
        request_id = parsed_data.get("requestId", "")


        if type_req == 'R_CI' and request_id == '1031': 
            id_carte = parsed_data.get("id_carte", "")
            date_ex = parsed_data.get("date_exp", "").strip()
            id_borne = parsed_data.get("id_borne", "").strip()
            date_exp = datetime.strptime(date_ex, "%d-%m-%Y")
            response = Check_carte(id_carte, date_exp)
            res_reponse = (
                f"response_type:{response.response_type} | "
                f"status_code:{response.status_code} | "
                f"action_code:{response.action_code} | "
                f"message:{response.message} | "
                f"timestamp:{response.timestamp}"
            )
            return res_reponse

        elif type_req == 'R_BRI' and request_id == '1001':
            id_borne = parsed_data.get("id_borne", "").strip()
            print(id_borne)
            id_station = parsed_data.get("id_station", "").strip()
            response = Check_borne(id_borne, id_station)
            res_reponse = (
                f"response_type:{response.response_type} | "
                f"status_code:{response.status_code} | "
                f"action_code:{response.action_code} | "
                f"message:{response.message} | "
                f"timestamp:{response.timestamp}"
            )
            return res_reponse

        elif type_req == 'R_JI' and request_id == '721':
            id_borne = parsed_data.get("id_borne", "").strip()
            print(id_borne)
            id_carte = parsed_data.get("id_carte", "")
            response = Update_data(id_carte, id_borne)
            res_reponse = (
                f"response_type:{response.response_type} | "
                f"status_code:{response.status_code} | "
                f"action_code:{response.action_code} | "
                f"message:{response.message} | "
                f"timestamp:{response.timestamp}"
            )
            return res_reponse


        else:
            return 'REIV|201|256|2433|Request malformed|'

    except Exception as e:
        return f'REIV|301|256|2433|Server error: {str(e)}|'


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}...')

        while True:
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                data = conn.recv(1024).decode()  # Receive request from client

                if not data:
                    break

                print(f"Received request: {data}")
                
                response = handle_request(data)  # Process the request
                print(f"Sending response: {response}")

                conn.sendall(response.encode())  # Send response to client

if __name__ == '__main__':
    run_server()
