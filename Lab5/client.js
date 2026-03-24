const net = require('net');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function sendRequest() {
    const client = new net.Socket();

    client.connect(8080, '127.0.0.1', () => {
        rl.question('Введите два числа через запятую (напр. 15.5, 30): ', (answer) => {
            client.write(answer);
        });
    });

    client.on('data', (data) => {
        console.log(`\n[ОТВЕТ СЕРВЕРА]: ${data.toString()}`);
        client.destroy();
        sendRequest(); // Повторяем для удобства тестирования
    });

    client.on('error', (err) => {
        console.log(`\n[ОШИБКА]: ${err.message}. Возможно сервер выключен.`);
        process.exit();
    });
}

console.log("=== Тестовый клиент для ЛР №5 (Circuit Breaker) ===");
sendRequest();
