from fastapi import FastAPI, HTTPException
import uvicorn

# Створення екземпляра додатка з назвою для документації Swagger
app = FastAPI(
    title="String Processor API (Variant 2)",
    description="API для розвороту рядків (Лабораторна робота №1)",
    version="1.0.0"
)

# Клас бізнес-логіки згідно з Варіантом №2
class StringProcessor:
    def reverse_string(self, value: str) -> str:
        """
        Основна функція обробки: приймає рядок та повертає його в зворотному порядку.
        Використовує Python slicing [::-1].
        """
        if value is None:
            return ""
        return value[::-1]

# Ініціалізація об'єкта логіки
processor = StringProcessor()

@app.get("/process")
async def process(value: str = ""):
    """
    HTTP GET ендпоїнт для обробки запитів від клієнта.
    
    Параметри:
    - value: вхідний рядок для реверсу (через Query String)
    
    Повертає JSON з результатом або помилку 500 при збої.
    """
    try:
        # Виклик методу реверсу
        processed_result = processor.reverse_string(value)
        
        # Повернення успішної відповіді у форматі JSON
        return {
            "status": "success",
            "input": value,
            "result": processed_result
        }
    except Exception as e:
        # Обробка виняткових ситуацій
        raise HTTPException(
            status_code=500, 
            detail=f"Внутрішня помилка сервера: {str(e)}"
        )

# Точка входу для запуску сервера
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("Сервер FastAPI успішно запущено!")
    print("Документація (Swagger) доступна за адресою: http://127.0.0.1:8000/docs")
    print("Натисніть Ctrl+C для зупинки.")
    print("--------------------------------------------------")
    
    # Запуск сервера на локальному хості, порт 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)c
