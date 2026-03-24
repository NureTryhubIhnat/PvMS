const dgram = require('dgram');
const client = dgram.createSocket('udp4');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('UDP: Введіть числа через кому: ', (input) => {
    const message = Buffer.from(input);

    client.send(message, 8001, '127.0.0.1', (err) => {
        if (err) {
            console.error('Помилка надсилання');
            client.close();
        }
    });
});

client.on('message', (msg, rinfo) => {
    console.log(`Відповідь від сервера (UDP): ${msg.toString()}`);
    client.close();
    rl.close();
});
