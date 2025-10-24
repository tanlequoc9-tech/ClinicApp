# 🏥 Hệ thống Quản lý Phòng khám

## 📋 Yêu cầu hệ thống

- Python 3.7 trở lên
- pip (Python package installer)

## 🚀 Hướng dẫn cài đặt và chạy

### Bước 1: Tạo môi trường ảo (Virtual Environment)

**Trên macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Trên Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

> 💡 **Lưu ý:** Sau khi kích hoạt, bạn sẽ thấy `(venv)` xuất hiện trước dòng lệnh

### Bước 2: Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install flask flask-sqlalchemy
```

### Bước 3: Chạy ứng dụng

```bash
python app.py
```

### Bước 4: Truy cập ứng dụng

Mở trình duyệt và truy cập:

```
http://127.0.0.1:5000
```

hoặc

```
http://localhost:5000
```

## 🎯 Tính năng chính

- ✅ Quản lý bệnh nhân (Thêm, Sửa, Xóa)
- ✅ Quản lý lịch hẹn
- ✅ Thống kê dashboard
- ✅ Giao diện đẹp, hiện đại

## 📁 Cấu trúc thư mục

```
clinic-management/
├── app.py              # File chính của ứng dụng
├── models.py           # Định nghĩa database models
├── requirements.txt    # Danh sách thư viện
├── clinic.db          # Database SQLite (tự động tạo)
└── README.md          # File hướng dẫn này
```

## 🛠️ Khắc phục sự cố

### Lỗi: Module not found

```bash
pip install flask flask-sqlalchemy
```

### Lỗi: Database schema không khớp

```bash
# Xóa database cũ và tạo lại
rm clinic.db        # macOS/Linux
del clinic.db       # Windows

# Chạy lại app
python app.py
```

### Thoát môi trường ảo

```bash
deactivate
```

## 📝 Ghi chú

- Port mặc định: `5000`
- Database: SQLite (lưu tại `clinic.db`)
- Debug mode: Bật (tắt khi deploy production)

## 💬 Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:

1. Python đã cài đặt đúng chưa: `python --version`
2. Đã kích hoạt virtual environment chưa
3. Đã cài đặt đầy đủ thư viện chưa: `pip list`

---

**Chúc bạn sử dụng thành công! 🎉**
