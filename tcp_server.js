const net = require('net');

// Конфігурація сервера
const PORT = 8000;
const HOST = '127.0.0.1';

const server = net.createServer((socket) => {
    console.log(`[TCP] Клієнт підключився: ${socket.remoteAddress}:${socket.remotePort}`);

    socket.on('data', (data) => {
        const message = data.toString().trim();
        console.log(`[TCP] Отримано дані: ${message}`);

        try {
            // Парсинг двох чисел (очікується формат "число1,число2")
            const [num1, num2] = message.split(',').map(Number);
            
            if (isNaN(num1) || isNaN(num2)) {
                socket.write("Помилка: Надішліть два числа через кому (напр. 10,20)");
            } else {
                const sum = num1 + num2;
                console.log(`[TCP] Обчислення: ${num1} + ${num2} = ${sum}`);
                socket.write(sum.toString());
            }
        } catch (err) {
            socket.write("Помилка обробки даних");
        }
    });

    socket.on('end', () => {
        console.log('[TCP] Клієнт відключився');
    });

    socket.on('error', (err) => {
        console.error(`[TCP] Помилка сокета: ${err.message}`);
    });
});

server.listen(PORT, HOST, () => {
    console.log(`TCP Сервер запущено на ${HOST}:${PORT}`);
    console.log('Очікування підключень...');
});
