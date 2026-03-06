# FastAPI Social Media Backend 

A production-ready RESTful API built with **FastAPI**, focusing on security, scalability, and clean architecture. This project is currently the core backend for a full-stack social application.

## Tech Stack
*   **Framework:** [FastAPI](https://fastapi.tiangolo.com) (Python)
*   **Database:** [PostgreSQL](https://www.postgresql.org)
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org)
*   **Security:** JWT Authentication & OAuth2
*   **Validation:** Pydantic
*   **Environment:** Fedora Linux

## Key Features (Implemented)
- [x] **User Management:** Registration and Profile models.
- [x] **JWT Authentication:** Secure login with hashed passwords using `passlib`.
- [x] **Relational Database:** Structured PostgreSQL schemas with SQLAlchemy.
- [x] **Modular Routing:** Clean code separation using `APIRouter`.
- [x] **Offline Documentation:** Custom Swagger UI setup for offline development.

## Project Structure
```text
backend/
├── app/
│   ├── routers/    # API Endpoints (Users, Posts, Auth)
│   ├── models.py   # SQLAlchemy Database Models
│   ├── schemas.py  # Pydantic Data Validation
│   ├── oauth2.py   # JWT Logic & Security
│   └── main.py     # Application Entry Point
├── tests/          # Pytest Suite
└── requirements.txt

