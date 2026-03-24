const net = require('net');

/**
 * Конфігурація Circuit Breaker (Запобіжника)
 */
const CONFIG = {
    FAILURE_THRESHOLD: 3,      // Кількість помилок для спрацювання
    RECOVERY_TIMEOUT: 5000,    // Час очікування перед спробою відновлення (мс)
};

const STATES = {
    CLOSED: 'CLOSED',       // Працює у звичайному режимі
    OPEN: 'OPEN',           // Помилка, запити блокуються
    HALF_OPEN: 'HALF_OPEN'  // Пробний режим після збою
};

let currentState = STATES.CLOSED;
let failureCount = 0;
let nextAttemptTime = 0;

/**
 * Імітація асинхронного сервісу обчислень (Варіант 2: Сума)
 */
async function computeSumAsync(n1, n2) {
    return new Promise((resolve, reject) => {
        // Імітація мережевої затримки
        setTimeout(() => {
            const shouldFail = Math.random() < 0.3; // 30% шанс збою для тесту
            if (shouldFail) {
                reject(new Error("Помилка доступу до бази даних"));
            } else {
                resolve(n1 + n2);
            }
        }, 500);
    });
}

/**
 * Логіка перемикання станів запобіжника
 */
function handleFailure() {
    failureCount++;
    console.log(`[УВАГА] Зафіксовано збій #${failureCount}`);

    if (failureCount >= CONFIG.FAILURE_THRESHOLD) {
        currentState = STATES.OPEN;
        nextAttemptTime = Date.now() + CONFIG.RECOVERY_TIMEOUT;
        console.log(`[КРИТИЧНО] Запобіжник перейшов у стан OPEN. Блокування на ${CONFIG.RECOVERY_TIMEOUT/1000}с`);
    }
}

function handleSuccess() {
    if (currentState === STATES.HALF_OPEN) {
        console.log(`[ІНФО] Тестовий запит успішний. Систему відновлено. Стан: CLOSED`);
    }
    failureCount = 0;
    currentState = STATES.CLOSED;
}

const server = net.createServer((socket) => {
    console.log(`[МЕРЕЖА] Нове підключення від ${socket.remoteAddress}`);

    socket.on('data', async (data) => {
        const input = data.toString().trim();
        
        // 1. Перевірка стану запобіжника
        if (currentState === STATES.OPEN) {
            if (Date.now() > nextAttemptTime) {
                currentState = STATES.HALF_OPEN;
                console.log("[ІНФО] Час очікування минув. Спроба переведення в HALF_OPEN...");
            } else {
                socket.write("ПОМИЛКА_СЕРВЕРА: Запобіжник ВІДКРИТО. Спробуйте пізніше.\n");
                return;
            }
        }

        try {
            const [n1, n2] = input.split(',').map(Number);

            if (isNaN(n1) || isNaN(n2)) {
                socket.write("ПОМИЛКА_ВВОДУ: Надішліть числа у форматі '10,20'\n");
                return;
            }

            // 2. Асинхронний виклик (Варіант 2)
            const result = await computeSumAsync(n1, n2);

            // 3. Обробка успіху
            handleSuccess();
            socket.write(`УСПІХ: Результат ${result}\n`);
            console.log(`[ЛОГ] Успішне обчислення: ${n1} + ${n2} = ${result}`);

        } catch (error) {
            handleFailure();
            socket.write(`ПОМИЛКА_СЕРВЕРА: ${error.message}\n`);
            console.error(`[ПОМИЛКА] Стався збій: ${error.message}`);
        }
    });
});

server.listen(8080, '127.0.0.1', () => {
    console.log("--------------------------------------------------");
    console.log("Асинхронний TCP сервер (Варіант 2) працює на 8080");
    console.log(`Поточний стан запобіжника: ${currentState}`);
    console.log("--------------------------------------------------");
});
