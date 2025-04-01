import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
DATABASE = os.getenv("DATABASE_URL", "attendance.db")
