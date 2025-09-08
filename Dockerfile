FROM python:3.10-slim

# Встановлюємо залежності для Chromium
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Python-залежності
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . /app

# Вказуємо змінну середовища для Selenium
ENV PATH="/usr/lib/chromium:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Запускаємо головний файл
CMD ["python", "main.py"]
