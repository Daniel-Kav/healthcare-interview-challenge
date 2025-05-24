# Healthcare Appointment Scheduling System

A Django-based healthcare appointment scheduling system that allows patients to book appointments with doctors, manage medical records, and handle doctor availability.

## Features

- User authentication and authorization (Patients, Doctors, Admins)
- Patient profile management
- Doctor profile and availability management
- Appointment scheduling with conflict prevention
- Medical records management
- RESTful API with Swagger documentation
- JWT authentication
- Role-based access control

## Tech Stack

- Backend: Django 5.2.1
- Database: PostgreSQL
- API Documentation: Swagger/OpenAPI
- Authentication: JWT
- Task Queue: Celery with Redis
- Frontend: React (separate repository)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd healthcare-interview-challenge
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/healthcare_db
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Start Celery worker (in a separate terminal):
```bash
celery -A healthcaresystem worker -l info
```

9. Start Redis server (required for Celery)

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Testing

Run the test suite:
```bash
python manage.py test
```

## Project Structure

```
healthcaresystem/
├── doctors/           # Doctor management app
├── patients/          # Patient management app
├── appointments/      # Appointment scheduling app
├── users/            # User authentication and management
└── healthcaresystem/ # Project settings and configuration
```

## Security Features

- JWT-based authentication
- Role-based access control
- Secure password hashing
- CORS protection
- Input validation
- SQL injection prevention
- XSS protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 