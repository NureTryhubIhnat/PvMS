import socket
import threading
from collections import deque

# Налаштування
HOST = '127.0.0.1'
PORT = 65432
FIELD_SIZE = 100
WIN_COUNT = 5

field = [[' ' for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
request_queue = deque(maxlen=50)
lock = threading.Lock()

def check_winner(r, c, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # В обидва боки від останнього ходу
        for step in [1, -1]:
            nr, nc = r + dr*step, c + dc*step
            while 0 <= nr < FIELD_SIZE and 0 <= nc < FIELD_SIZE and field[nr][nc] == symbol:
                count += 1
                nr += dr*step
                nc += dc*step
        if count >= WIN_COUNT:
            return True
    return False

def process_queue():
    while True:
        if request_queue:
            with lock:
                addr, symbol, r, c = request_queue.popleft()
                if field[r][c] == ' ':
                    field[r][c] = symbol
                    print(f"Обробка: {symbol} на [{r},{c}]. Черга: {len(request_queue)}")
                    if check_winner(r, c, symbol):
                        print(f"ГРАВЕЦЬ {symbol} ПЕРЕМІГ!")
                else:
                    print(f"Позиція [{r},{c}] вже зайнята.")

# Запуск обробника черги в окремому потоці
threading.Thread(target=process_queue, daemon=True).start()

# Налаштування UDP сокета
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Сервер запущено на {HOST}:{PORT}. Очікування запитів...")
    
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(',') # Формат: СИМВОЛ,РЯДОК,СТОВПЕЦЬ
        if len(msg) == 3:
            sym, r, c = msg[0], int(msg[1]), int(msg[2])
            with lock:
                if len(request_queue) < 50:
                    request_queue.append((addr, sym, r, c))
                else:
                    print("Черга переповнена!")
