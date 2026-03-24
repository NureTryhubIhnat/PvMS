const net = require('net');
const client = new net.Socket();

const PORT = 8000;
const HOST = '127.0.0.1';

client.connect(PORT, HOST, () => {
    console.log('Підключено до сервера в Docker');
    client.write('15.5,26.5'); // Тестові дані
});

client.on('data', (data) => {
    console.log(`Результат від сервера: ${data.toString()}`);
    client.destroy();
});
