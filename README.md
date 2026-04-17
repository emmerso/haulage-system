# Haulage Truck Management System

A REST API system for managing haulage trucks, drivers, and delivery jobs.


## Tech Stack
- Python 3.11
- Django 5.1.4
- Django REST Framework
- PostgreSQL 15
- Docker & Docker Compose

---

## Getting Started

### Prerequisites
Only one thing needed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/haulage-system.git
cd haulage-system
```

### 2. Run the Project
```bash
docker-compose up --build
```
The API will be available at: **http://127.0.0.1:8000**

### 3. Create Your Admin User
Open a second terminal in the same folder and run:
```bash
docker-compose exec web python manage.py createsuperuser
```
Enter your chosen username, email and password when prompted.

---

## Authentication

All endpoints require a token. Get yours by calling the login endpoint.

**POST** `http://127.0.0.1:8000/api/auth/login/`

Request body:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Include this token in every request header:
```
Authorization: Token your_token_here
```

---

## API Endpoints

### Trucks
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/trucks/ | List all trucks |
| POST | /api/trucks/ | Register a new truck |
| GET | /api/trucks/{id}/ | Get a single truck |
| PUT | /api/trucks/{id}/ | Update a truck |
| DELETE | /api/trucks/{id}/ | Delete a truck |

**Truck fields:**
```json
{
    "registration_number": "ZW 123 ABC",
    "capacity": 10000,
    "status": "AVAILABLE"
}
```
Status options: `AVAILABLE`, `IN_TRANSIT`, `UNDER_MAINTENANCE`

---

### Drivers
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/drivers/ | List all drivers |
| POST | /api/drivers/ | Add a new driver |
| GET | /api/drivers/{id}/ | Get a single driver |
| PUT | /api/drivers/{id}/ | Update a driver |
| DELETE | /api/drivers/{id}/ | Delete a driver |

**Driver fields:**
```json
{
    "name": "Tendai Moyo",
    "license_number": "ZW-DL-4521",
    "phone_number": "0772345678"
}
```

---

### Jobs
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/jobs/ | List all jobs |
| POST | /api/jobs/ | Create a new job |
| GET | /api/jobs/{id}/ | Get a single job |
| PUT | /api/jobs/{id}/ | Update a job |
| DELETE | /api/jobs/{id}/ | Delete a job |

**Job fields:**
```json
{
    "pickup_location": "Harare CBD",
    "delivery_location": "Bulawayo",
    "cargo_description": "50 bags of cement",
    "status": "PENDING",
    "assigned_truck": 1,
    "assigned_driver": 1
}
```
Status options: `PENDING`, `IN_TRANSIT`, `DELIVERED`, `CANCELLED`

---

## Business Rules

- Trucks with status `IN_TRANSIT` or `UNDER_MAINTENANCE` cannot be assigned to a job
- Drivers with an active `IN_TRANSIT` job cannot be assigned to another job
- When a job status changes to `IN_TRANSIT` the assigned truck automatically becomes `IN_TRANSIT`
- When a job status changes to `DELIVERED` or `CANCELLED` the truck automatically returns to `AVAILABLE`

---

## Running Tests
```bash
python manage.py test
```
Expected output:
```
Ran 14 tests in 0.543s
OK
```

---

## Features Implemented
- Full CRUD for Trucks, Drivers and Jobs
- Token Authentication
- Pagination (10 items per page)
- Request Logging to haulage.log
- Unit Tests (14 tests)
- PostgreSQL database
- Docker containerization

---

## Project Structure
```
haulage_system/
├── core/               # Django settings and main URLs
├── trucks/             # Truck management app
├── drivers/            # Driver management app
├── jobs/               # Job management app
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```