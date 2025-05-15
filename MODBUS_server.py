import socket
from scapy.all import *

MODBUS_PORT = 502

def handle_modbus_request(request):
    print(request)
    # Parse the Modbus request
    transaction_id = request[0:2]
    protocol_id = request[2:4]
    length = request[4:6]
    unit_id = request[6:7]
    function_code = request[7:8]

    # Create a basic Modbus response
    if function_code == b'\x01':  # Function code 01: Read Coils
        
        coil_status = b'\x01'  # coil status (ON)
        length = b'\x00\x04'  # Length of the response data
        response = transaction_id + protocol_id + length + unit_id + function_code + b'\x01' + coil_status

    elif function_code == b'\x03':  # Function code 03: Read Holding Registers
    
        register_value = b'\x00\x64'  # register value (100)
        length = b'\x00\x05'  # Length of the response data
        response = transaction_id + protocol_id + length + unit_id + function_code + b'\x02' + register_value
    
    elif function_code == b'\x04':  # Function code 04: Read Input Registers
        NUM_REGISTERS = 10
        byte_count = (2 * NUM_REGISTERS).to_bytes(1, byteorder='big')
    
        # Generate simulated register values (2 bytes each)
        register_values = b''.join(
           [(1000 + i).to_bytes(2, byteorder='big') for i in range(NUM_REGISTERS)]
        )
    
        # Length field (2 bytes): Number of remaining bytes (unit_id + function_code + byte_count + data)
        length = (1 + 1 + 1 + len(register_values)).to_bytes(2, byteorder='big')
        response = transaction_id + protocol_id + length + unit_id + function_code + byte_count + register_values
        print(response)

    elif function_code == b'\x05':  # Function code 05: Write Single Coil
        coil_address = b'\x00\x01'  
        coil_value = b'\xFF\x00' 
        length = b'\x00\x06'
        response = transaction_id + protocol_id + length + unit_id + function_code + coil_address + coil_value
    
    elif function_code == b'\x06':  # Function code 06: Write Single Register
        register_value = b'\x00\x64' 
        length = b'\x00\x06'
        response = transaction_id + protocol_id + length + unit_id + function_code + b'\x00\x01' + register_value

    elif function_code == b'\x0F':  # Function code 15: Write Multiple Coils
        # calculate the length
        length = b'\x00\x06'    
        ref_num = request[8:10]
        byte_count = request[10:12]
    
        response = transaction_id + protocol_id + length + unit_id + function_code + ref_num + byte_count# this includes reference number and byte count at network level 

    elif function_code == b'\x10':  # Function code 16: Write Multiple Registers
        length = b'\x00\x06'
        ref_num = request[8:10]
        byte_count = request[10:12]
        
        response = transaction_id + protocol_id + length + unit_id + function_code + ref_num + byte_count# this includes reference number and byte count at network level
    elif function_code == b'\x11': # Function code 17: Report Slave ID
        # length of the response
        length = b'\x00\x0B'
        slave_id = b'\x01'
        slave_name = b'\x4D\x6F\x64\x62\x75\x73\x20\x53\x65\x72\x76\x65\x72' # Modbus Server
        response = transaction_id + protocol_id + length + unit_id + function_code + slave_id + slave_name
    
    else:
        # Handle other function codes if needed
        response = transaction_id + protocol_id + b'\x00\x03' + unit_id +function_code+ b'\x83' + b'\x01'  # Exception response

    print(response)
    return response

def start_modbus_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', MODBUS_PORT))
    server_socket.listen(5)

    print(f"Listening for Modbus TCP connections on port {MODBUS_PORT}...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            # Receive the request
            request = client_socket.recv(1024)
            if not request:
                break

            # Process the Modbus request
            response_data = handle_modbus_request(request)

            # Send the response back 
            client_socket.sendall(response_data)

        finally:
            # Clean up the connection
            client_socket.close()

if __name__ == "__main__":
    start_modbus_server()