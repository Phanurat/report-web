from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime

# โหลดค่าจากไฟล์ .env
load_dotenv()

# สร้างแอป Flask
app = Flask(__name__)

# กำหนดค่า secret_key
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# ตั้งค่าฐานข้อมูล SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# สร้างฐานข้อมูล
db = SQLAlchemy(app)

# สร้าง LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# สร้างโมเดล User และ Attendance
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_in = db.Column(db.String(100), nullable=False)
    time_out = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', back_populates='attendances')

User.attendances = db.relationship('Attendance', back_populates='user')

# โหลดผู้ใช้จาก ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ฟังก์ชันเพื่อดึงเวลาปัจจุบันใน timezone ประเทศไทย
def get_time_in_thailand():
    thailand_tz = pytz.timezone('Asia/Bangkok')
    return datetime.now(thailand_tz).strftime('%Y-%m-%d %H:%M:%S')

# หน้าแรก (home)
@app.route('/')
def home():
    return render_template('home.html')

# หน้า Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# หน้า Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ตรวจสอบว่าชื่อผู้ใช้ซ้ำไหม
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists, please choose another one."
        
        # สร้างผู้ใช้ใหม่
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # ล็อกอินและเปลี่ยนไปยัง Dashboard
        login_user(new_user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

# หน้า Dashboard หลังจากล็อกอิน
@app.route('/dashboard')
@login_required
def dashboard():
    # บันทึกเวลาเข้า
    if request.args.get('action') == 'time_in':
        time_in = get_time_in_thailand()  # รับเวลาปัจจุบันในโซนเวลาไทย
        new_attendance = Attendance(user_id=current_user.id, time_in=time_in)
        db.session.add(new_attendance)
        db.session.commit()
    elif request.args.get('action') == 'time_out':
        time_out = get_time_in_thailand()  # รับเวลาปัจจุบันในโซนเวลาไทย
        attendance = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.id.desc()).first()
        attendance.time_out = time_out
        db.session.commit()

    # แสดงข้อมูลการเข้าออกงาน
    attendances = Attendance.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', attendances=attendances)

# หน้า Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
