from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
from models import db, Patient, Doctor, Appointment
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Khởi tạo dữ liệu mẫu nếu database trống
        if not Doctor.query.first():
            sample_doctors = [
                Doctor(name='Nguyễn Văn An', specialty='Nội khoa'),
                Doctor(name='Trần Thị Bình', specialty='Nhi khoa'),
                Doctor(name='Lê Minh Châu', specialty='Da liễu'),
            ]
            db.session.add_all(sample_doctors)
            db.session.commit()

    # ==================== TEMPLATES ====================
    
    BASE_STYLE = """
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1e40af;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #ea580c;
            --light: #f8fafc;
            --dark: #1e293b;
            --border: #e2e8f0;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            color: var(--primary);
            font-size: 28px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .nav-links {
            display: flex;
            gap: 16px;
        }
        .nav-links a {
            padding: 10px 20px;
            background: var(--light);
            color: var(--dark);
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
        }
        .nav-links a:hover, .nav-links a.active {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        .stat-card .icon {
            width: 56px;
            height: 56px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 16px;
        }
        .stat-card h3 {
            font-size: 32px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 8px;
        }
        .stat-card p {
            color: #64748b;
            font-size: 14px;
            font-weight: 500;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 24px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--border);
        }
        .card-title {
            font-size: 22px;
            font-weight: 700;
            color: var(--dark);
        }
        .btn {
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
        }
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        .btn-primary:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }
        .btn-success {
            background: var(--success);
            color: white;
        }
        .btn-danger {
            background: var(--danger);
            color: white;
        }
        .btn-warning {
            background: var(--warning);
            color: white;
        }
        .btn-sm {
            padding: 6px 16px;
            font-size: 13px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
            font-size: 14px;
        }
        .form-control {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        .table-container {
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        thead {
            background: var(--light);
        }
        th {
            padding: 14px 16px;
            text-align: left;
            font-weight: 600;
            color: var(--dark);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        td {
            padding: 16px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }
        tr:hover {
            background: #f8fafc;
        }
        .badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }
        .badge-primary { background: #dbeafe; color: var(--primary); }
        .badge-success { background: #dcfce7; color: var(--success); }
        .badge-danger { background: #fee2e2; color: var(--danger); }
        .alert {
            padding: 14px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        .alert-success {
            background: #dcfce7;
            color: var(--success);
            border-left: 4px solid var(--success);
        }
        .alert-danger {
            background: #fee2e2;
            color: var(--danger);
            border-left: 4px solid var(--danger);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            animation: fadeIn 0.3s;
        }
        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 32px;
            border-radius: 16px;
            width: 90%;
            max-width: 600px;
            animation: slideDown 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .action-buttons {
            display: flex;
            gap: 8px;
        }
    </style>
    """

    DASHBOARD_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trang chủ - Phòng khám</title>
        """ + BASE_STYLE + """
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 Hệ thống Quản lý Phòng khám</h1>
                <div class="nav-links">
                    <a href="{{ url_for('index') }}" class="active">Trang chủ</a>
                    <a href="{{ url_for('patients') }}">Bệnh nhân</a>
                    <a href="{{ url_for('appointments') }}">Lịch hẹn</a>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon" style="background: #dbeafe; color: #2563eb;">👥</div>
                    <h3>{{ patients_count }}</h3>
                    <p>Tổng bệnh nhân</p>
                </div>
                <div class="stat-card">
                    <div class="icon" style="background: #dcfce7; color: #16a34a;">👨‍⚕️</div>
                    <h3>{{ doctors_count }}</h3>
                    <p>Bác sĩ</p>
                </div>
                <div class="stat-card">
                    <div class="icon" style="background: #fef3c7; color: #ea580c;">📅</div>
                    <h3>{{ upcoming_count }}</h3>
                    <p>Lịch hẹn sắp tới</p>
                </div>
                <div class="stat-card">
                    <div class="icon" style="background: #e9d5ff; color: #9333ea;">✅</div>
                    <h3>{{ today_count }}</h3>
                    <p>Lịch hẹn hôm nay</p>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Chào mừng đến với hệ thống quản lý phòng khám</h2>
                </div>
                <p style="color: #64748b; line-height: 1.8; margin-bottom: 24px;">
                    Hệ thống giúp bạn quản lý bệnh nhân, bác sĩ và lịch hẹn một cách hiệu quả. 
                    Giao diện thân thiện, dễ sử dụng với đầy đủ tính năng thêm, sửa, xóa.
                </p>
                <div style="display: flex; gap: 12px;">
                    <a href="{{ url_for('patients') }}" class="btn btn-primary">Quản lý bệnh nhân</a>
                    <a href="{{ url_for('appointments') }}" class="btn btn-success">Quản lý lịch hẹn</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    PATIENTS_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quản lý Bệnh nhân</title>
        """ + BASE_STYLE + """
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>👥 Quản lý Bệnh nhân</h1>
                <div class="nav-links">
                    <a href="{{ url_for('index') }}">Trang chủ</a>
                    <a href="{{ url_for('patients') }}" class="active">Bệnh nhân</a>
                    <a href="{{ url_for('appointments') }}">Lịch hẹn</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div style="display: grid; grid-template-columns: 2fr 3fr; gap: 24px;">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">{{ 'Cập nhật bệnh nhân' if edit_patient else 'Thêm bệnh nhân mới' }}</h2>
                    </div>
                    <form method="POST" action="{{ url_for('patient_edit', id=edit_patient.id) if edit_patient else url_for('patients') }}">
                        <div class="form-group">
                            <label class="form-label">Họ và tên *</label>
                            <input type="text" name="name" class="form-control" 
                                   value="{{ edit_patient.name if edit_patient else '' }}" required>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Số điện thoại</label>
                                <input type="text" name="phone" class="form-control" 
                                       value="{{ edit_patient.phone if edit_patient else '' }}">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Ngày sinh</label>
                                <input type="date" name="date_of_birth" class="form-control" 
                                       value="{{ edit_patient.date_of_birth if edit_patient else '' }}">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Địa chỉ</label>
                            <input type="text" name="address" class="form-control" 
                                   value="{{ edit_patient.address if edit_patient else '' }}">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Ghi chú</label>
                            <textarea name="notes" class="form-control" rows="3">{{ edit_patient.notes if edit_patient else '' }}</textarea>
                        </div>
                        <div style="display: flex; gap: 12px;">
                            <button type="submit" class="btn btn-primary">
                                {{ '💾 Cập nhật' if edit_patient else '➕ Thêm mới' }}
                            </button>
                            {% if edit_patient %}
                                <a href="{{ url_for('patients') }}" class="btn btn-warning">Hủy</a>
                            {% endif %}
                        </div>
                    </form>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">Danh sách bệnh nhân ({{ patients|length }})</h2>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Họ tên</th>
                                    <th>SĐT</th>
                                    <th>Tuổi</th>
                                    <th>Địa chỉ</th>
                                    <th>Thao tác</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for p in patients %}
                                <tr>
                                    <td><strong>#{{ p.id }}</strong></td>
                                    <td>{{ p.name }}</td>
                                    <td>{{ p.phone or '-' }}</td>
                                    <td>{{ p.age if p.age else '-' }}</td>
                                    <td>{{ p.address or '-' }}</td>
                                    <td>
                                        <div class="action-buttons">
                                            <a href="{{ url_for('patient_edit', id=p.id) }}" class="btn btn-primary btn-sm">✏️ Sửa</a>
                                            <form method="POST" action="{{ url_for('patient_delete', id=p.id) }}" 
                                                  onsubmit="return confirm('Xác nhận xóa bệnh nhân {{ p.name }}?')" style="display: inline;">
                                                <button type="submit" class="btn btn-danger btn-sm">🗑️ Xóa</button>
                                            </form>
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    APPOINTMENTS_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quản lý Lịch hẹn</title>
        """ + BASE_STYLE + """
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📅 Quản lý Lịch hẹn</h1>
                <div class="nav-links">
                    <a href="{{ url_for('index') }}">Trang chủ</a>
                    <a href="{{ url_for('patients') }}">Bệnh nhân</a>
                    <a href="{{ url_for('appointments') }}" class="active">Lịch hẹn</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Tạo lịch hẹn mới</h2>
                </div>
                <form method="POST">
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Bệnh nhân *</label>
                            <select name="patient_id" class="form-control" required>
                                <option value="">-- Chọn bệnh nhân --</option>
                                {% for p in patients %}
                                    <option value="{{ p.id }}">{{ p.display_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Bác sĩ *</label>
                            <select name="doctor_id" class="form-control" required>
                                <option value="">-- Chọn bác sĩ --</option>
                                {% for d in doctors %}
                                    <option value="{{ d.id }}">{{ d.display_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Ngày hẹn *</label>
                            <input type="date" name="date" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Giờ hẹn *</label>
                            <input type="time" name="time" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Trạng thái</label>
                            <select name="status" class="form-control">
                                <option value="scheduled">Đã đặt</option>
                                <option value="completed">Hoàn thành</option>
                                <option value="cancelled">Đã hủy</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Lý do khám</label>
                        <input type="text" name="reason" class="form-control">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Ghi chú</label>
                        <textarea name="notes" class="form-control" rows="2"></textarea>
                    </div>
                    <button type="submit" class="btn btn-success">➕ Tạo lịch hẹn</button>
                </form>
            </div>

            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Danh sách lịch hẹn ({{ appointments|length }})</h2>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Thời gian</th>
                                <th>Bệnh nhân</th>
                                <th>Bác sĩ</th>
                                <th>Lý do</th>
                                <th>Trạng thái</th>
                                <th>Thao tác</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for a in appointments %}
                            <tr>
                                <td><strong>#{{ a.id }}</strong></td>
                                <td>{{ a.formatted_datetime }}</td>
                                <td>{{ a.patient.display_name }}</td>
                                <td>{{ a.doctor.display_name }}</td>
                                <td>{{ a.reason or '-' }}</td>
                                <td><span class="badge badge-{{ a.status_badge }}">{{ a.status_text }}</span></td>
                                <td>
                                    <form method="POST" action="{{ url_for('appointment_delete', id=a.id) }}" 
                                          onsubmit="return confirm('Xác nhận xóa lịch hẹn này?')" style="display: inline;">
                                        <button type="submit" class="btn btn-danger btn-sm">🗑️ Xóa</button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

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
            flash(f'✅ Thêm bệnh nhân {name} thành công!', 'success')
            return redirect(url_for('patients'))
        
        patients_list = Patient.query.order_by(Patient.created_at.desc()).all()
        return render_template_string(
            PATIENTS_TEMPLATE,
            patients=patients_list,
            edit_patient=None
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
            flash(f'✅ Cập nhật thông tin bệnh nhân {patient.name} thành công!', 'success')
            return redirect(url_for('patients'))
        
        patients_list = Patient.query.order_by(Patient.created_at.desc()).all()
        return render_template_string(
            PATIENTS_TEMPLATE,
            patients=patients_list,
            edit_patient=patient
        )

    @app.route('/patients/delete/<int:id>', methods=['POST'])
    def patient_delete(id):
        patient = Patient.query.get_or_404(id)
        name = patient.name
        db.session.delete(patient)
        db.session.commit()
        flash(f'✅ Đã xóa bệnh nhân {name}!', 'success')
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
            flash('✅ Tạo lịch hẹn thành công!', 'success')
            return redirect(url_for('appointments'))
        
        appointments_list = Appointment.query.order_by(
            Appointment.appointment_datetime.desc()
        ).all()
        patients_list = Patient.query.order_by(Patient.name).all()
        doctors_list = Doctor.query.order_by(Doctor.name).all()
        
        return render_template_string(
            APPOINTMENTS_TEMPLATE,
            appointments=appointments_list,
            patients=patients_list,
            doctors=doctors_list
        )

    @app.route('/appointments/delete/<int:id>', methods=['POST'])
    def appointment_delete(id):
        appointment = Appointment.query.get_or_404(id)
        db.session.delete(appointment)
        db.session.commit()
        flash('✅ Đã xóa lịch hẹn!', 'success')
        return redirect(url_for('appointments'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)