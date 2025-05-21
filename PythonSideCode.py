## 2. Python Client (Position Monitoring Only)

import socket
import time
from typing import Optional, Tuple

class ABBPositionMonitor:
    def __init__(self, ip: str = "192.168.125.1", port: int = 3000):
        self.ip = ip
        self.port = port
        self.socket = None
        
    def connect(self) -> bool:
        """Establish connection to robot"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def get_position(self) -> Optional[Tuple[float, float, float]]:
        """Get current robot position (x,y,z) in mm"""
        try:
            data = self.socket.recv(1024).decode().strip()
            x, y, z = map(float, data.split(','))
            return (x, y, z)
        except Exception as e:
            print(f"Error reading position: {e}")
            return None
    
    def close(self):
        """Close connection"""
        if self.socket:
            self.socket.close()

# Usage Example
if __name__ == "__main__":
    monitor = ABBPositionMonitor()
    
    if monitor.connect():
        try:
            while True:
                position = monitor.get_position()
                if position:
                    x, y, z = position
                    print(f"X: {x:.1f} mm | Y: {y:.1f} mm | Z: {z:.1f} mm")
                time.sleep(0.1)  # Adjust polling rate
        except KeyboardInterrupt:
            print("Stopping monitoring...")
        finally:
            monitor.close()
