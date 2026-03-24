const net = require('net');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const client = new net.Socket();

client.connect(8000, '127.0.0.1', () => {
    console.log('Підключено до TCP сервера');
    
    rl.question('Введіть два числа через кому (наприклад, 12.5, 7): ', (input) => {
        client.write(input);
    });
});

client.on('data', (data) => {
    console.log(`Відповідь від сервера (Сума): ${data.toString()}`);
    client.destroy(); // Закриваємо з'єднання після отримання відповіді
});

client.on('close', () => {
    console.log('З\'єднання закрите. Натисніть Ctrl+C для виходу.');
    rl.close();
});

client.on('error', (err) => {
    console.error('Помилка підключення. Переконайтеся, що сервер запущено.');
    rl.close();
});
