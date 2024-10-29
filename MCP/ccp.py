from utils import create_socket, send_message, receive_message, log_event
import random

def start_ccp(ccp_id):
    print(f"Starting CCP for Blade Runner {ccp_id}...")
    ccp_socket = create_socket(3001)  # Using port 2002 to listen and send messages
    send_initialization(ccp_socket, ccp_id)

    while True:
        print("Waiting for MCP commands...")
        message, _ = receive_message(ccp_socket)
        handle_mcp_command(message, ccp_id)

# def send_initialization(socket, ccp_id):
#     init_message = {
#         "client_type": "ccp",
#         "message": "CCIN",
#         "client_id": ccp_id
#     }
#     print(f"Sending initialization message to MCP: {init_message}")
#     send_message(("127.0.0.1", 2000, ), init_message)  # Use correct MCP IP address
def send_initialization(socket, ccp_id):
    init_message = {
        "client_type": "ccp",
        "message": "CCIN",
        "client_id": ccp_id,
        "sequence_number": random.randint(1000, 30000)  # Ensure it includes a sequence number
    }
    print(f"Sending initialization message to MCP: {init_message}")
    send_message(("127.0.0.1", 2000), init_message)  # Use correct MCP IP address

def handle_mcp_command(message, ccp_id):
    log_event("MCP Command Received", message)
    
    action = message.get('action')
    
    if action == "FFASTC":
        handle_move_forward(ccp_id)
    
    elif action == "STOPO":
        handle_stopo(ccp_id)
    
    elif action == "STOPC":
        handle_stopc(ccp_id)
    
    elif action == "MOVE_TO_NEXT_BLOCK":
        handle_move_to_next_block(ccp_id)
    
    elif action == "FSLOWC":
        handle_slow_forward(ccp_id, message.get('turn_severity', 0))  # Using default 0 severity
    
    elif action == "RSLOWC":
        handle_slow_reverse(ccp_id, message.get('turn_severity', 0))  # Using default 0 severity
    
    elif action == "EMERGENCY_STOP":
        handle_emergency_stop(ccp_id)
    
    elif action == "RSLOWC":
        handle_door_control(message['action'], ccp_id)
    
    elif action == "IRLD":
        handle_ir_led(message['status'], ccp_id)

    elif action == "TRIP":
        handle_beam_break_sensor(ccp_id)
    
    else:
        print(f"Unknown command received: {message}")

def handle_move_forward(ccp_id):
    print(f"BR {ccp_id} starting as per MCP command.")
    send_status_update(ccp_id, "moving forward")
def handle_stopo(ccp_id):
    print(f"BR {ccp_id} stopping as per MCP command.")
    send_status_update(ccp_id, "stopped - doors open")
def handle_stopc(ccp_id):
    print(f"BR {ccp_id} stopping as per MCP command.")
    send_status_update(ccp_id, "stopped - doors closed")
def handle_move_to_next_block(ccp_id):
    print(f"BR {ccp_id} moving to the next block as per MCP command.")
    send_status_update(ccp_id, "moved_to_next_block")

def handle_slow_forward(ccp_id, severity):
    print(f"BR {ccp_id} slowing down for turn with severity {severity}.")
    send_status_update(ccp_id, f"slowed_for_turn_severity_{severity}")

def handle_slow_reverse(ccp_id, severity):
    print(f"BR {ccp_id} slowing down for turn with severity {severity}.")
    send_status_update(ccp_id, f"slowed_for_turn_severity_{severity}")

def handle_emergency_stop(ccp_id):
    print(f"BR {ccp_id} performing emergency stop as per MCP command.")
    send_status_update(ccp_id, "emergency_stopped")

def handle_door_control(action, ccp_id):
    print(f"BR {ccp_id} doors are being {action} as per MCP command.")
    send_status_update(ccp_id, f"doors_{action}")

def handle_ir_led(status, ccp_id):
    print(f"IR LED for BR {ccp_id} is being turned {status} as per MCP command.")
    send_status_update(ccp_id, f"ir_led_{status}")

def handle_beam_break_sensor(ccp_id):
    print(f"Beam break sensor tripped for BR {ccp_id}.")
    send_status_update(ccp_id, "beam_break_sensor_tripped")

def send_status_update(ccp_id, status):
    status_message = {
        "client_type": "ccp",
        "message": "STAT",
        "client_id": ccp_id,
        "status": status
    }
    print(f"Sending status update to MCP: {status_message}")
    send_message(("192.168.1.101", 2000), status_message)  # Use correct MCP IP address

if __name__ == "__main__":
    start_ccp("BR01")
