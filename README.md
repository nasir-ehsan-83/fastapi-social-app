# FastAPI Social Media Application 

A production-ready RESTful API built with **FastAPI**, focusing on security, scalability, and clean architecture. This project is currently the core backend for a full-stack social application.

---

## Project Structure
```
fastapi-social-app
│
├── backend/
│   ├── app/
│   │   ├── core/    
│   │   ├── db/ 
│   │   ├── models/ 
│   │   ├── routers/ 
│   │   ├── schemas/
│   │   ├── service/  
│   │   ├── __init__.py
│   │   └── main.py    
│   │
│   ├── tests/ 
│   ├── fastapi_offline_docs/ 
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
├── LICENSE
└── README.md
```

---

## Tech Stack
*   **Framework:** [FastAPI](https://fastapi.tiangolo.com) (Python)
*   **Database:** [PostgreSQL](https://www.postgresql.org)
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org)
*   **Security:** JWT Authentication & OAuth2
*   **Validation:** Pydantic
*   **Environment:** Fedora Linux

---

## Key Features
- [ ] **User Management:** Registration and Profile models.
- [ ] **JWT Authentication:** Secure login with hashed passwords using `passlib`.
- [ ] **Relational Database:** Structured PostgreSQL schemas with SQLAlchemy.
- [ ] **Modular Routing:** Clean code separation using `APIRouter`.
- [ ] **Offline Documentation:** Custom Swagger UI setup for offline development.

---

## Author

**Nasir Ahmad Ehsan**

**Interested in:**
- Backend Development
- Programming Languages
- Artificial Intelligence
- Operating System Design