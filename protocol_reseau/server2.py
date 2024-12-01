import socket
from datetime import datetime
import logging

from Cheching import Check_carte, Check_borne, Update_data, Check_station, Respond_LastUse
from BDD_Server_connection import read_config

# Read config file
config = read_config(r"protocol_reseau\Config.conf")
HOST = config.get("host")
PORT = int(config.get("port", 0))

print(HOST, PORT)
isConnected = False

# Setup logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Protocol order
PROTOCOL_SEQUENCE = ['R_BRI', 'R_ST', 'R_CI', 'R_DU', 'R_JI']

# Dictionary to track the protocol state of each client
client_states = {}

def parse_message(data):
    try:
        # Split fields and parse key-value pairs
        fields = data.split('|')
        parsed_data = {key_value.split(':')[0]: key_value.split(':')[1] for key_value in fields if ':' in key_value}
        return parsed_data
    except Exception as e:
        raise ValueError(f"Error parsing message: {str(e)}")

def handle_request(data, client_address):
    global isConnected
    
    # Initialize the client's protocol state if not already tracked
    if client_address not in client_states:
        client_states[client_address] = 0  # Start with the first step of the protocol
    try:
        # Parse the incoming request
        parsed_data = parse_message(data)

        # Extract values
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

            # Enforce protocol sequence
            if current_protocol_step >= len(PROTOCOL_SEQUENCE) or type_req != PROTOCOL_SEQUENCE[current_protocol_step]:
                return f"response_type:REIV | status_code:400 | action_code:2433 | message:Vous ne suivez pas le protocole | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Process the current request and advance the protocol step
            if type_req == 'R_BRI' and request_id == '1001':
                id_borne = parsed_data.get("id_borne", "").strip()
                id_station = parsed_data.get("id_station", "").strip()
                response = Check_borne(id_borne, id_station)
                client_states[client_address] += 1  # Advance to the next step
                return format_response(response)

            elif type_req == 'R_ST' and request_id == '1021':
                id_station = parsed_data.get("id_station", "").strip()
                response = Check_station(id_station)
                client_states[client_address] += 1  # Advance to the next step
                return format_response(response)

            elif type_req == 'R_CI' and request_id == '1031':
                id_carte = parsed_data.get("id_carte", "").strip()
                date_ex = parsed_data.get("date_exp", "").strip()
                date_exp = datetime.strptime(date_ex, "%Y-%m-%d")
                response = Check_carte(id_carte, date_exp)
                client_states[client_address] += 1  # Advance to the next step
                return format_response(response)

            elif type_req == 'R_DU' and request_id == '1041':
                id_carte = parsed_data.get("id_carte", "").strip()
                response = Respond_LastUse(id_carte)
                client_states[client_address] += 1  # Advance to the next step
                return format_response(response)

            elif type_req == 'R_JI' and request_id == '721':
                id_borne = parsed_data.get("id_borne", "").strip()
                id_carte = parsed_data.get("id_carte", "").strip()
                response = Update_data(id_carte, id_borne)
                client_states.pop(client_address, None)  # End of protocol, reset state
                return format_response(response)

            else:
                return f"response_type:REIV | status_code:400 | action_code:2433 | message:Request malformed | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        else:
            return f"response_type:REIV | status_code:403 | action_code:2433 | message:No connection detected | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    except Exception as e:
        return f"response_type:REIV | status_code:500 | action_code:2433 | message:Server error: {str(e)} | timestamp:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def format_response(response):
    """Formats the response object into a string."""
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
        print(f'Server listening on {HOST}:{PORT}...')
        logging.info(f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            logging.info(f"Connection established with {addr}")
            print(f"Connected by {addr}")
            conn.settimeout(20)  # Set the timeout to 20 seconds

            try:
                while True:
                    data = conn.recv(1024).decode()  # Receive request from client
                    if not data:  # Handle client disconnection
                        logging.info(f"Client {addr} disconnected.")
                        print(f"Client {addr} disconnected.")
                        break

                    logging.info(f"Received request from {addr}: {data}")
                    print(f"Received request: {data}")

                    # Process the request
                    response = handle_request(data, addr)

                    response = f"{response}\n"  # Add newline
                    conn.sendall(response.encode("utf-8"))  # Send response
                    logging.info(f"Sending response to {addr}: {response}")
                    print(f"Sending response: {response}")

            except Exception as e:
                logging.error(f"Error handling client {addr}: {e}")
                print(f"Error handling client {addr}: {e}")
            finally:
                conn.close()
                logging.info(f"Connection with {addr} closed.")
                print(f"Connection with {addr} closed.")

if __name__ == '__main__':
    run_server()
