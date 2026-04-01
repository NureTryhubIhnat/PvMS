import socket
import random
import time

HOST = '127.0.0.1'
PORT = 65432
SYMBOLS = ['X', '0']

def send_move():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        
        # Імітація серії випадкових ходів
        for _ in range(1000):
            symbol = random.choice(SYMBOLS)
            row = random.randint(0, 99)
            col = random.randint(0, 99)
            
            message = f"{symbol},{row},{col}"
            s.sendto(message.encode(), (HOST, PORT))
            print(f"Відправлено: {message}")
            time.sleep(0.01) # Невелика затримка для наочності

if __name__ == "__main__":
    send_move()
