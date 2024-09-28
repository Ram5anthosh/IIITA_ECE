import socket
import time
from datetime import datetime
from real_time_processing import process_river_path, path_planning, detect_waste_sites  # Assumes pre-built ML models
from non_real_time_processing import get_river_path # satellite image processing using rApp
# Command dictionary for controlling the drone
cmds = {
    'START_MISSION': 'DRONE_START_MISSION',
    'STOP_MISSION': 'DRONE_STOP_MISSION',
    'NEXT_STEP' : 'DRONE_CALIBRATE_DIRECTION',
    'TAKE_IMAGE': 'DRONE_TAKE_IMAGE',
    'MARK_LOCATION': 'DRONE_MARK_LOCATION',
    'MOVE_TO_NEXT': 'DRONE_MOVE_TO_NEXT_POINT',
    'RETURN_BASE': 'DRONE_RETURN_TO_BASE'
}

class XApp:
    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.river_path = None
        self.drone_status = "IDLE"
    
    def send_request(self, message):
        """Send a message to the RAN node or drone to request data or issue commands."""
        self.conn.send(f"{message} at {datetime.now().strftime('%H:%M:%S')}".encode('utf-8'))
    
    def receive_data(self):
        """Receive image or I/Q data from the RAN node."""
        data = self.conn.recv(16384)
        if data:
            print(f"Received data at {datetime.now().strftime('%H:%M:%S')}")
            return data
        return None
    
    def process_data(self, data):
        """Run ML algorithms and  on received data to detect river paths."""
        if process_river_path(data):
            self.river_path = data  # Store detected river path
            print("River path identified.")
            self.next_step = path_planning(data)
            print("Next Step computed.")
        else:
            print("River path not detected, retrying...")

       # Send images to Non-RealTime Processing to check for waste and marking location  
        if self.river_path:
            waste_detected = detect_waste_sites(self.river_path)
            if waste_detected:
                print("Waste sites detected along river.")
                self.send_request(cmds['MARK_LOCATION'])
                return True
            else:
                print("No waste detected.")
        return False
    
    def run(self):
        """Main loop to run the xApp and control the drone."""
        while True:
            # Start mission
            self.send_request(cmds['START_MISSION'])
            
            # Receive satellite image or sensor data
            data = self.receive_data()
            if data:
                # Process the data using ML models
                if self.process_data(data):
                    # If waste is detected, move drone to next location
                    self.send_request(cmds['MOVE_TO_NEXT'])
                else:
                    # No waste detected, stop the mission or retry
                    self.send_request(cmds['RETURN_BASE'])
            
            time.sleep(1)  # Sleep before checking for next data
            
            # You can add conditions to stop the mission
            if self.drone_status == "RETURNED":
                break
    
    def stop(self):
        """Stop the xApp."""
        self.send_request(cmds['STOP_MISSION'])
        self.conn.close()

if __name__ == "__main__":
    xapp = XApp(ip="192.168.1.1", port=8080)
    try:
        xapp.run()
    except KeyboardInterrupt:
        xapp.stop()
