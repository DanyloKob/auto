# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Додай свої cookies тут
COOKIES = [
    {
        "domain": "console.sryzen.com",
        "hostOnly": True,
        "httpOnly": True,
        "name": "flux.sid",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "yUJVT7o5DfTywVkQ5fgBN-2UhvGLhh8c"
    },
    {
        "domain": "console.sryzen.com",
        "hostOnly": True,
        "httpOnly": True,
        "name": "connect.sid",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "s%3AsfSGYWx78IKqJGI0Ag4VVqsHOqpepAQG.xg1MmCsOvYwwfJDA3UtG9tmo030PHtK8HlXSe40oTKY"
    }
]

# Функція для навігації та завантаження кукі-файлів
def navigate_and_load_cookies(driver, cookies):
    """
    Переходить на початкову сторінку, завантажує кукі-файли
    і потім переходить на цільову сторінку.
    """
    try:
        # Спочатку переходимо на базовий домен для встановлення cookies
        driver.get("https://console.sryzen.com/")
        
        if cookies:
            for cookie in cookies:
                # Видаляємо несумісні атрибути перед додаванням
                cookie.pop('sameSite', None)
                cookie.pop('expirationDate', None)
                cookie.pop('session', None)
                cookie.pop('storeId', None)
                cookie.pop('hostOnly', None)
                driver.add_cookie(cookie)
            print("✅ Cookies успішно завантажено.")
        else:
            print("⚠️ Cookies не знайдено. Будь ласка, вставте їх у код.")
            return False

        # Переходимо на правильну цільову сторінку
        driver.get("https://console.sryzen.com/coins/afk")
        print("Перехід на сторінку AFK...")
        time.sleep(5)  # Даємо сторінці час на повне завантаження
        return True
    except Exception as e:
        print(f"❌ Помилка під час навігації або завантаження cookies: {e}")
        return False

# Головна функція бота
def run_afk_bot():
    print("🤖 Бот запущений!")

    # Налаштування WebDriver для Chrome
    chrome_options = Options()
    # Якщо хочеш бачити вікно браузера, закоментуй наступний рядок
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")  # Приховати зайві логи

    chrome_options.binary_location = "/usr/bin/chromium-browser"


    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Помилка при запуску браузера: {e}")
        return

    try:
        # Початкова навігація та завантаження кукі-файлів
        if not navigate_and_load_cookies(driver, COOKIES):
            driver.quit()
            return
        
        while True:
            print("Очікування 10 секунд. Шукаю статус...")
            time.sleep(10)

            try:
                # Шукаємо елемент, який містить текст "Connected" або "Disconnected"
                status_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Connected') or contains(text(), 'Disconnected')]")
                status_text = status_element.text
                print(f"📊 Поточний статус: {status_text}")

                if "Disconnected" in status_text:
                    print("❌ Виявлено 'Disconnected'. Повторна навігація та завантаження сторінки...")
                    if not navigate_and_load_cookies(driver, COOKIES):
                         print("Повторна навігація не вдалася, зупиняю бота.")
                         break
                elif "Connected" in status_text:
                    print("🟢 Підключено! Починаю прокручування сторінки...")
                    
                    # Виконуємо прокручування для імітації активності
                    for _ in range(200):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(3)
                    
                    print("Прокручування завершено. Чекаю наступної перевірки...")
                else:
                    print("⚠️ Невідомий статус. Повторна навігація...")
                    if not navigate_and_load_cookies(driver, COOKIES):
                         print("Повторна навігація не вдалася, зупиняю бота.")
                         break

            except NoSuchElementException:
                print("⚠️ Не вдалося знайти статусний елемент. Можливо, структура сторінки змінилася. Повторна навігація...")
                if not navigate_and_load_cookies(driver, COOKIES):
                     print("Повторна навігація не вдалася, зупиняю бота.")
                     break
            except Exception as e:
                print(f"❌ Сталася неочікувана помилка: {e}")
                break
                
    except Exception as e:
        print(f"❌ Критична помилка під час роботи бота: {e}")
        
    finally:
        print("\n🏁 Бот завершив роботу!")
        if 'driver' in locals():
            driver.quit()

# Запускаємо бота
if __name__ == "__main__":
    run_afk_bot()
