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
## Running with Docker (Optional)

1. Build the Docker image:
    
    ```
    docker build -t fastapi-app .
    ```
    
2. Run the container:
    
    ```
     docker run -d --name fastapi-container-1 -p 8000:8000 fastapi-app
    ```
    ```
    docker exec 5c1b1a2015ddcc6d9958933e36c728bad34f6700e920ba8aa6fb1e69f822807e /bin/sh
    ```

    
