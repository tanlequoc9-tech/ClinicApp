# templates.py - All HTML templates for the Flask application

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Phòng khám{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px 0;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(20px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: none;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-8px);
        }
        
        .stat-card .display-4 {
            font-weight: 700;
        }
        
        .btn {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        .table {
            background: white;
        }
        
        .badge {
            padding: 8px 12px;
            font-weight: 600;
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light mb-4">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="bi bi-hospital"></i> Phòng khám
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'index' %}active fw-bold{% endif %}" href="{{ url_for('index') }}">
                            <i class="bi bi-house"></i> Trang chủ
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint in ['patients', 'patient_edit'] %}active fw-bold{% endif %}" href="{{ url_for('patients') }}">
                            <i class="bi bi-people"></i> Bệnh nhân
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'appointments' %}active fw-bold{% endif %}" href="{{ url_for('appointments') }}">
                            <i class="bi bi-calendar-check"></i> Lịch hẹn
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} alert-dismissible fade show" role="alert">
                        <i class="bi bi-{{ 'check-circle' if category == 'success' else 'exclamation-triangle' }}"></i>
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Content -->
    {% block content %}{% endblock %}

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ==================== DASHBOARD TEMPLATE ====================
DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    {% block content %}
    <div class="container">
        <!-- Statistics -->
        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="card stat-card text-center p-4">
                    <i class="bi bi-people display-1"></i>
                    <h2 class="display-4 mt-3">{{ patients_count }}</h2>
                    <p class="text-uppercase mb-0">Tổng bệnh nhân</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card text-center p-4" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <i class="bi bi-person-badge display-1"></i>
                    <h2 class="display-4 mt-3">{{ doctors_count }}</h2>
                    <p class="text-uppercase mb-0">Bác sĩ</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card text-center p-4" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <i class="bi bi-calendar-event display-1"></i>
                    <h2 class="display-4 mt-3">{{ upcoming_count }}</h2>
                    <p class="text-uppercase mb-0">Lịch hẹn sắp tới</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card text-center p-4" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <i class="bi bi-check-circle display-1"></i>
                    <h2 class="display-4 mt-3">{{ today_count }}</h2>
                    <p class="text-uppercase mb-0">Lịch hẹn hôm nay</p>
                </div>
            </div>
        </div>

        <!-- Welcome Card -->
        <div class="card">
            <div class="card-body p-5">
                <h2 class="card-title mb-4">
                    <i class="bi bi-hospital text-primary"></i>
                    Chào mừng đến với hệ thống quản lý phòng khám
                </h2>
                <p class="lead text-muted mb-4">
                    Hệ thống giúp bạn quản lý bệnh nhân, bác sĩ và lịch hẹn một cách hiệu quả và chuyên nghiệp. 
                    Giao diện thân thiện, hiện đại với đầy đủ tính năng thêm, sửa, xóa.
                </p>
                <div class="d-flex gap-3">
                    <a href="{{ url_for('patients') }}" class="btn btn-primary btn-lg">
                        <i class="bi bi-people"></i> Quản lý bệnh nhân
                    </a>
                    <a href="{{ url_for('appointments') }}" class="btn btn-success btn-lg">
                        <i class="bi bi-calendar-check"></i> Quản lý lịch hẹn
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
""")

# ==================== PATIENTS TEMPLATE ====================
PATIENTS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    {% block content %}
    <div class="container">
        <div class="row g-4">
            <!-- Form -->
            <div class="col-lg-4">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-{{ 'pencil-square' if edit_patient else 'person-plus' }}"></i>
                            {{ 'Cập nhật bệnh nhân' if edit_patient else 'Thêm bệnh nhân mới' }}
                        </h5>
                    </div>
                    <div class="card-body">
                        <form method="POST" action="{{ url_for('patient_edit', id=edit_patient.id) if edit_patient else url_for('patients') }}">
                            <div class="mb-3">
                                <label class="form-label">Họ và tên <span class="text-danger">*</span></label>
                                <input type="text" name="name" class="form-control" 
                                       value="{{ edit_patient.name if edit_patient else '' }}" 
                                       placeholder="Nguyễn Văn A" required>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Số điện thoại</label>
                                <input type="text" name="phone" class="form-control" 
                                       value="{{ edit_patient.phone if edit_patient else '' }}"
                                       placeholder="0123456789">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Ngày sinh</label>
                                <input type="date" name="date_of_birth" class="form-control" 
                                       value="{{ edit_patient.date_of_birth if edit_patient else '' }}">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Địa chỉ</label>
                                <input type="text" name="address" class="form-control" 
                                       value="{{ edit_patient.address if edit_patient else '' }}"
                                       placeholder="123 Đường ABC, Quận XYZ">
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Ghi chú</label>
                                <textarea name="notes" class="form-control" rows="3" 
                                          placeholder="Thông tin thêm...">{{ edit_patient.notes if edit_patient else '' }}</textarea>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-{{ 'save' if edit_patient else 'plus-lg' }}"></i>
                                    {{ 'Cập nhật' if edit_patient else 'Thêm mới' }}
                                </button>
                                {% if edit_patient %}
                                    <a href="{{ url_for('patients') }}" class="btn btn-secondary">
                                        <i class="bi bi-x-lg"></i> Hủy
                                    </a>
                                {% endif %}
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- List -->
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-list-ul"></i>
                            Danh sách bệnh nhân ({{ patients|length }})
                        </h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Họ tên</th>
                                        <th>SĐT</th>
                                        <th>Tuổi</th>
                                        <th>Địa chỉ</th>
                                        <th class="text-end">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for p in patients %}
                                    <tr>
                                        <td><strong>#{{ p.id }}</strong></td>
                                        <td><strong>{{ p.name }}</strong></td>
                                        <td>{{ p.phone or '-' }}</td>
                                        <td>{{ p.age if p.age else '-' }}</td>
                                        <td>{{ p.address or '-' }}</td>
                                        <td class="text-end">
                                            <a href="{{ url_for('patient_edit', id=p.id) }}" class="btn btn-sm btn-primary">
                                                <i class="bi bi-pencil"></i>
                                            </a>
                                            <form method="POST" action="{{ url_for('patient_delete', id=p.id) }}" 
                                                  onsubmit="return confirm('Xác nhận xóa bệnh nhân {{ p.name }}?')" 
                                                  class="d-inline">
                                                <button type="submit" class="btn btn-sm btn-danger">
                                                    <i class="bi bi-trash"></i>
                                                </button>
                                            </form>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
""")

# ==================== APPOINTMENTS TEMPLATE ====================
APPOINTMENTS_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    {% block content %}
    <div class="container">
        <!-- Form -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">
                    <i class="bi bi-calendar-plus"></i>
                    Tạo lịch hẹn mới
                </h5>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="row g-3">
                        <div class="col-md-4">
                            <label class="form-label">Bệnh nhân <span class="text-danger">*</span></label>
                            <select name="patient_id" class="form-select" required>
                                <option value="">-- Chọn bệnh nhân --</option>
                                {% for p in patients %}
                                    <option value="{{ p.id }}">{{ p.display_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="col-md-4">
                            <label class="form-label">Bác sĩ <span class="text-danger">*</span></label>
                            <select name="doctor_id" class="form-select" required>
                                <option value="">-- Chọn bác sĩ --</option>
                                {% for d in doctors %}
                                    <option value="{{ d.id }}">{{ d.display_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="col-md-4">
                            <label class="form-label">Trạng thái</label>
                            <select name="status" class="form-select">
                                <option value="scheduled">Đã đặt</option>
                                <option value="completed">Hoàn thành</option>
                                <option value="cancelled">Đã hủy</option>
                            </select>
                        </div>
                        
                        <div class="col-md-6">
                            <label class="form-label">Ngày hẹn <span class="text-danger">*</span></label>
                            <input type="date" name="date" class="form-control" required>
                        </div>
                        
                        <div class="col-md-6">
                            <label class="form-label">Giờ hẹn <span class="text-danger">*</span></label>
                            <input type="time" name="time" class="form-control" required>
                        </div>
                        
                        <div class="col-md-12">
                            <label class="form-label">Lý do khám</label>
                            <input type="text" name="reason" class="form-control" 
                                   placeholder="VD: Khám tổng quát, tái khám...">
                        </div>
                        
                        <div class="col-md-12">
                            <label class="form-label">Ghi chú</label>
                            <textarea name="notes" class="form-control" rows="2" 
                                      placeholder="Thông tin thêm..."></textarea>
                        </div>
                        
                        <div class="col-12">
                            <button type="submit" class="btn btn-success">
                                <i class="bi bi-plus-lg"></i> Tạo lịch hẹn
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- List -->
        <div class="card">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">
                    <i class="bi bi-list-ul"></i>
                    Danh sách lịch hẹn ({{ appointments|length }})
                </h5>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Thời gian</th>
                                <th>Bệnh nhân</th>
                                <th>Bác sĩ</th>
                                <th>Lý do</th>
                                <th>Trạng thái</th>
                                <th class="text-end">Thao tác</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for a in appointments %}
                            <tr>
                                <td><strong>#{{ a.id }}</strong></td>
                                <td><strong>{{ a.formatted_datetime }}</strong></td>
                                <td>{{ a.patient.display_name }}</td>
                                <td>{{ a.doctor.display_name }}</td>
                                <td>{{ a.reason or '-' }}</td>
                                <td>
                                    <span class="badge bg-{{ a.status_badge }}">
                                        {{ a.status_text }}
                                    </span>
                                </td>
                                <td class="text-end">
                                    <form method="POST" action="{{ url_for('appointment_delete', id=a.id) }}" 
                                          onsubmit="return confirm('Xác nhận xóa lịch hẹn này?')" 
                                          class="d-inline">
                                        <button type="submit" class="btn btn-sm btn-danger">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}
""")