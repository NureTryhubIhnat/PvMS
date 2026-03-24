const dgram = require('dgram');
const server = dgram.createSocket('udp4');

const PORT = 8001;
const HOST = '127.0.0.1';

server.on('error', (err) => {
    console.log(`[UDP] Помилка сервера:\n${err.stack}`);
    server.close();
});

server.on('message', (msg, rinfo) => {
    const message = msg.toString().trim();
    console.log(`[UDP] Отримано дейтаграму від ${rinfo.address}:${rinfo.port}: ${message}`);

    const [num1, num2] = message.split(',').map(Number);
    
    let response;
    if (isNaN(num1) || isNaN(num2)) {
        response = "Помилка формату";
    } else {
        const sum = num1 + num2;
        response = sum.toString();
        console.log(`[UDP] Результат обчислення: ${sum}`);
    }

    server.send(response, rinfo.port, rinfo.address, (err) => {
        if (err) console.error('[UDP] Помилка надсилання відповіді');
    });
});

server.on('listening', () => {
    const address = server.address();
    console.log(`UDP Сервер слухає на ${address.address}:${address.port}`);
});

server.bind(PORT, HOST);
