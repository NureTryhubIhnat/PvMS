import requests
import time

def main():
    # URL локального сервера (FastAPI)
    api_url = "http://127.0.0.1:8000/process"
    
    print("=== HTTP Клієнт: Варіант №2 (Реверс рядка) ===")
    print("Для виходу введіть 'exit' або натисніть Ctrl+C\n")

    while True:
        # Отримання вводу від користувача
        user_input = input("Введіть текст для відправки на сервер: ")

        if user_input.lower() == 'exit':
            print("Завершення роботи клієнта...")
            break

        try:
            # Виконання HTTP GET запиту з параметрами (Query Parameters)
            # Наприклад: http://127.0.0.1:8000/process?value=текст
            response = requests.get(api_url, params={"value": user_input}, timeout=5)

            # Перевірка статус-коду відповіді
            if response.status_code == 200:
                # Десеріалізація JSON відповіді
                data = response.json()
                print(f" -> [Сервер]: {data['result']}")
            else:
                print(f" -> [Помилка]: Сервер повернув статус {response.status_code}")

        except requests.exceptions.ConnectionError:
            print(" -> [Помилка]: Не вдалося з'єднатися з сервером. Переконайтеся, що server.py запущено.")
        except Exception as e:
            print(f" -> [Помилка]: Сталася непередбачувана помилка: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    main()
