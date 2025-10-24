from flask import Flask, render_template_string, request, redirect, url_for, flash
from models import db, Patient, Doctor, Appointment
from datetime import datetime
from templates import (
    DASHBOARD_TEMPLATE,
    PATIENTS_TEMPLATE,
    APPOINTMENTS_TEMPLATE
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if not Doctor.query.first():
            sample_doctors = [
                Doctor(name='Nguyễn Văn An', specialty='Nội khoa'),
                Doctor(name='Trần Thị Bình', specialty='Nhi khoa'),
                Doctor(name='Lê Minh Châu', specialty='Da liễu'),
            ]
            db.session.add_all(sample_doctors)
            db.session.commit()

    # ==================== ROUTES ====================
    
    @app.route('/')
    def index():
        patients_count = Patient.query.count()
        doctors_count = Doctor.query.count()
        today = datetime.now().date()
        upcoming_count = Appointment.query.filter(
            Appointment.appointment_datetime >= datetime.now(),
            Appointment.status == 'scheduled'
        ).count()
        today_count = Appointment.query.filter(
            db.func.date(Appointment.appointment_datetime) == today
        ).count()
        
        return render_template_string(
            DASHBOARD_TEMPLATE,
            patients_count=patients_count,
            doctors_count=doctors_count,
            upcoming_count=upcoming_count,
            today_count=today_count
        )

    @app.route('/patients', methods=['GET', 'POST'])
    def patients():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            dob_str = request.form.get('date_of_birth', '').strip()
            notes = request.form.get('notes', '').strip()
            
            if not name:
                flash('Vui lòng nhập tên bệnh nhân!', 'danger')
                return redirect(url_for('patients'))
            
            dob = None
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except:
                    pass
            
            new_patient = Patient(
                name=name,
                phone=phone,
                address=address,
                date_of_birth=dob,
                notes=notes
            )
            db.session.add(new_patient)
            db.session.commit()
            flash(f'Thêm bệnh nhân {name} thành công!', 'success')
            return redirect(url_for('patients'))
        
        # TÌM KIẾM BỆNH NHÂN
        search = request.args.get('search', '').strip()
        query = Patient.query
        
        if search:
            search_filter = db.or_(
                Patient.name.ilike(f'%{search}%'),
                Patient.phone.ilike(f'%{search}%'),
                Patient.address.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        patients_list = query.order_by(Patient.created_at.desc()).all()
        
        return render_template_string(
            PATIENTS_TEMPLATE,
            patients=patients_list,
            edit_patient=None,
            search=search
        )

    @app.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
    def patient_edit(id):
        patient = Patient.query.get_or_404(id)
        
        if request.method == 'POST':
            patient.name = request.form.get('name', '').strip()
            patient.phone = request.form.get('phone', '').strip()
            patient.address = request.form.get('address', '').strip()
            dob_str = request.form.get('date_of_birth', '').strip()
            patient.notes = request.form.get('notes', '').strip()
            
            if dob_str:
                try:
                    patient.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except:
                    patient.date_of_birth = None
            
            db.session.commit()
            flash(f'Cập nhật thông tin bệnh nhân {patient.name} thành công!', 'success')
            return redirect(url_for('patients'))
        
        patients_list = Patient.query.order_by(Patient.created_at.desc()).all()
        return render_template_string(
            PATIENTS_TEMPLATE,
            patients=patients_list,
            edit_patient=patient,
            search=''
        )

    @app.route('/patients/delete/<int:id>', methods=['POST'])
    def patient_delete(id):
        patient = Patient.query.get_or_404(id)
        name = patient.name
        db.session.delete(patient)
        db.session.commit()
        flash(f'Đã xóa bệnh nhân {name}!', 'success')
        return redirect(url_for('patients'))

    @app.route('/appointments', methods=['GET', 'POST'])
    def appointments():
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            doctor_id = request.form.get('doctor_id')
            date_str = request.form.get('date', '').strip()
            time_str = request.form.get('time', '').strip()
            status = request.form.get('status', 'scheduled')
            reason = request.form.get('reason', '').strip()
            notes = request.form.get('notes', '').strip()
            
            if not all([patient_id, doctor_id, date_str, time_str]):
                flash('Vui lòng điền đầy đủ thông tin!', 'danger')
                return redirect(url_for('appointments'))
            
            try:
                appointment_dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
            except:
                flash('Định dạng ngày giờ không hợp lệ!', 'danger')
                return redirect(url_for('appointments'))
            
            new_appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_datetime=appointment_dt,
                status=status,
                reason=reason,
                notes=notes
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Tạo lịch hẹn thành công!', 'success')
            return redirect(url_for('appointments'))
        
        # LỌC LỊCH HẸN
        query = Appointment.query
        
        # Lọc theo ngày
        date_from = request.args.get('date_from', '').strip()
        date_to = request.args.get('date_to', '').strip()
        
        if date_from:
            try:
                from_dt = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(Appointment.appointment_datetime >= from_dt)
            except:
                pass
        
        if date_to:
            try:
                to_dt = datetime.strptime(date_to, '%Y-%m-%d')
                to_dt = to_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Appointment.appointment_datetime <= to_dt)
            except:
                pass
        
        # Lọc theo trạng thái
        status_filter = request.args.get('status', '').strip()
        if status_filter:
            query = query.filter(Appointment.status == status_filter)
        
        # Lọc theo bác sĩ
        doctor_filter = request.args.get('doctor_id', '').strip()
        if doctor_filter:
            query = query.filter(Appointment.doctor_id == doctor_filter)
        
        # Lọc theo bệnh nhân (tìm kiếm tên)
        patient_search = request.args.get('patient_search', '').strip()
        if patient_search:
            query = query.join(Patient).filter(
                Patient.name.ilike(f'%{patient_search}%')
            )
        
        appointments_list = query.order_by(
            Appointment.appointment_datetime.desc()
        ).all()
        
        patients_list = Patient.query.order_by(Patient.name).all()
        doctors_list = Doctor.query.order_by(Doctor.name).all()
        
        return render_template_string(
            APPOINTMENTS_TEMPLATE,
            appointments=appointments_list,
            patients=patients_list,
            doctors=doctors_list,
            date_from=date_from,
            date_to=date_to,
            status_filter=status_filter,
            doctor_filter=doctor_filter,
            patient_search=patient_search
        )

    @app.route('/appointments/delete/<int:id>', methods=['POST'])
    def appointment_delete(id):
        appointment = Appointment.query.get_or_404(id)
        db.session.delete(appointment)
        db.session.commit()
        flash('Đã xóa lịch hẹn!', 'success')
        return redirect(url_for('appointments'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)