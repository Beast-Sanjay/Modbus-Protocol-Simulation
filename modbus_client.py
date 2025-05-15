from telnetlib import IP
from scapy.all import *
from scapy.contrib.modbus import *

# Function to send a Read Holding Registers Request
def send_read_holding_registers_request(server_ip, server_port, unit_id, start_address, quantity_of_registers):
    # Craft the Modbus request
    request = ModbusADURequest(
        unit_id=unit_id
    ) / ModbusPDU03ReadHoldingRegistersRequest(
        starting_address=start_address,
        quantity_of_registers=quantity_of_registers
    )

    # Send the request and wait for the response
    response = sr1(IP(dst=server_ip)/TCP(dport=server_port)/request, iface='enp0s18')  # Use appropriate network interface

    # Check if a response was received
    if response:
        if response.haslayer(ModbusPDU03ReadHoldingRegistersResponse):
            registers = response[ModbusPDU03ReadHoldingRegistersResponse].regval
            print(f"Received response with registers: {registers}")
        else:
            print("Received a response, but it was not a Read Holding Registers Response.")
    else:
        print("No response received from the server.")

# Main function to run the client
if __name__ == "__main__":
    server_ip = ""  # Replace with the actual server IP if necessary
    server_port = 502
    unit_id = 1
    start_address = 0  # Starting address for reading registers
    quantity_of_registers = 10  # Number of registers to read

    send_read_holding_registers_request(server_ip, server_port, unit_id, start_address, quantity_of_registers)
