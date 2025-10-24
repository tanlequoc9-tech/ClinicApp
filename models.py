from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Patient {self.name}>'

    @property
    def display_name(self):
        """Hiển thị tên kèm số điện thoại"""
        return f"{self.name} ({self.phone})" if self.phone else self.name
    
    @property
    def age(self):
        """Tính tuổi từ ngày sinh"""
        if self.date_of_birth:
            today = datetime.today().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class Doctor(db.Model):
    __tablename__ = 'doctor'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120))
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.name}>'

    @property
    def display_name(self):
        """Hiển thị tên bác sĩ kèm chuyên khoa"""
        return f"BS. {self.name} - {self.specialty}" if self.specialty else f"BS. {self.name}"


class Appointment(db.Model):
    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    reason = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_datetime}>'

    @property
    def formatted_datetime(self):
        """Format datetime cho hiển thị"""
        return self.appointment_datetime.strftime('%d/%m/%Y %H:%M')
    
    @property
    def status_badge(self):
        """Trả về class badge cho status"""
        badges = {
            'scheduled': 'primary',
            'completed': 'success',
            'cancelled': 'danger'
        }
        return badges.get(self.status, 'secondary')
    
    @property
    def status_text(self):
        """Trả về text tiếng Việt cho status"""
        texts = {
            'scheduled': 'Đã đặt',
            'completed': 'Hoàn thành',
            'cancelled': 'Đã hủy'
        }
        return texts.get(self.status, 'Không xác định')