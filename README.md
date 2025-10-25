# AI Agent CRUD API

Dự án mẫu triển khai API CRUD với [FastAPI](https://fastapi.tiangolo.com/) và [SQLAlchemy](https://www.sqlalchemy.org/). Ứng dụng cung cấp các endpoint để quản lý danh sách mặt hàng, với cơ chế cấu hình qua biến môi trường và ví dụ test tự động bằng Pytest.

## Yêu cầu môi trường

- Python 3.11 trở lên
- `pip` hoặc trình quản lý gói tương đương

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows dùng: .venv\\Scripts\\activate
pip install -e .
# Cài thêm phụ thuộc dành cho phát triển
pip install -e .[dev]
```

## Chạy kiểm thử

```bash
pytest
```

## Khởi chạy ứng dụng

```bash
uvicorn app.main:app --reload
```

Ứng dụng sẽ khả dụng tại `http://127.0.0.1:8000`. Bạn có thể truy cập tài liệu tương tác tại `http://127.0.0.1:8000/docs`.

## Cấu hình

Các biến cấu hình chính được định nghĩa trong `app/core/config.py`. Bạn có thể tạo file `.env` ở thư mục gốc để ghi đè các giá trị mặc định:

```
APP_NAME=My CRUD API
DATABASE_URL=sqlite+aiosqlite:///./data.db
```

## Kiến trúc

- `app/main.py`: Khởi tạo FastAPI app, khai báo router và sự kiện khởi động.
- `app/api/routes.py`: Định nghĩa các endpoint CRUD cho tài nguyên Item.
- `app/models.py`: Định nghĩa schema cơ sở dữ liệu bằng SQLAlchemy ORM.
- `app/schemas.py`: Định nghĩa schema Pydantic cho request/response.
- `app/crud.py`: Xử lý logic thao tác dữ liệu.
- `tests/test_items_api.py`: Bộ kiểm thử tích hợp API.
