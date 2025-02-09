# انتخاب تصویر پایه
FROM python:3.10-slim

# نصب Git
RUN apt-get update && apt-get install -y git

# دایرکتوری کاری
WORKDIR /app

# کلون کردن ریپازیتوری گیت‌هاب
RUN git clone https://github.com/mehrab5869/1.git .

# نصب نیازمندی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای فایل اصلی
CMD ["python", "bot.py"]
