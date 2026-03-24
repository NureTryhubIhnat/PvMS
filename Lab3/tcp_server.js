const net = require('net');

const PORT = 8000;
const HOST = '0.0.0.0'; // Важливо для Docker, щоб приймати зовнішні підключення

const server = net.createServer((socket) => {
    console.log(`[TCP] Підключено: ${socket.remoteAddress}:${socket.remotePort}`);

    socket.on('data', (data) => {
        const message = data.toString().trim();
        const [num1, num2] = message.split(',').map(Number);
        
        if (!isNaN(num1) && !isNaN(num2)) {
            const sum = num1 + num2;
            console.log(`[TCP] Обчислення: ${num1} + ${num2} = ${sum}`);
            socket.write(sum.toString());
        } else {
            socket.write("Error: Please send numbers in format 'num1,num2'");
        }
    });
});

server.listen(PORT, HOST, () => {
    console.log(`TCP Сервер працює в контейнері на порту ${PORT}`);
});
