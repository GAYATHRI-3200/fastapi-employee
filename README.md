# FastAPI Employee Management API

CRUD API with:
- FastAPI
- Git
- Postman
- Docker
- CI (GitHub Actions)

Run locally:
```
uvicorn app:app --reload
```

Docker:
```
docker build -t fastapi-employee .
docker run -p 8000:8000 fastapi-employee
```

View here: https://fastapi-employee.onrender.com/employees/