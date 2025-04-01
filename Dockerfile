# ใช้ Python 3.9 เป็น Base Image
FROM python:3.9-slim

# กำหนด Working Directory
WORKDIR /app

# คัดลอกไฟล์ทั้งหมดไปยัง Container
COPY . .

# ติดตั้ง Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# เปิด Port 5000
EXPOSE 5000

# รันแอป
CMD ["python", "app.py"]
