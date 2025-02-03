## Installation

### Prerequisites

- Python 
    
- PostgreSQL
    
- Docker (optional)
    

### Setup (Windows)

1. Clone the repository:
    
    ```
    git clone https://github.com/hamsini2643/CRUD-APP-API.git
    cd fastapi-app
    ```
    
2. Create a virtual environment and install dependencies:
    
    ```
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
    
3. Configure the `.env` file:
    
    ```
    DATABASE_CONNECTION_STRING="postgresql://postgres:dbpassword@host.docker.internal/dbname"
    SECRET_KEY=any random string
    ALGORITHM="HS256"    (hashing algorithm)
    ```
    
4. Run database migrations:
    
    ```
    python create_db()
    ```
    
5. Start the FastAPI application:
    
    ```
    uvicorn main:app --reload
    ```
## 6. Add Database Migrations with Alembic

Initialize Alembic:

```
alembic init alembic
```

Update `alembic.ini` with your database URL:

```
sqlalchemy.url = postgresql://postgres:dbpassword@localhost/dbname
```

Generate migrations:

```
alembic revision --autogenerate -m "Initial migration"
```

Apply migrations:

```
alembic upgrade head
```

--- 

