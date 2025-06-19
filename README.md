Library Microservice - Complete Codebase
📋 README.md
markdown# Library Management Microservice

A modern, scalable library management microservice built with FastAPI, MongoDB, and Docker. This service provides a complete RESTful API for managing books, authors, and categories with clean architecture principles.

## 🚀 Features

- **RESTful API** with automatic documentation (Swagger/OpenAPI)
- **MongoDB integration** with Beanie ODM for async operations
- **Clean Architecture** with separation of concerns (Controllers, Services, Repositories)
- **Dependency Injection** for better testability and maintainability
- **Docker support** for easy deployment
- **Professional code structure** following Python best practices
- **Comprehensive data validation** using Pydantic models
- **Error handling** with proper HTTP status codes

## 🛠 Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for document storage
- **Beanie** - Async MongoDB ODM based on Pydantic
- **Pydantic** - Data validation using Python type annotations
- **Motor** - Async MongoDB driver
- **Uvicorn** - ASGI server for running the application
- **Docker** - Containerization platform

## 🏗 Architecture
├── Controllers (HTTP Layer)     → Handle HTTP requests/responses
├── Services (Business Logic)    → Process business rules
├── Repositories (Data Access)   → Database operations
└── Models (Data Structure)      → Database schema definitions

## 📁 Project Structure
library-microservice/
├── app/
│   ├── controllers/           # HTTP endpoints and request handling
│   ├── services/             # Business logic layer
│   │   └── impl/            # Service implementations
│   ├── repositories/         # Data access layer
│   ├── models/              # Database models (Beanie documents)
│   ├── schemas/             # Pydantic schemas for validation
│   ├── config/              # Configuration files
│   ├── dependencies.py      # Dependency injection setup
│   └── main.py             # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Multi-container setup
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md            # Project documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MongoDB (Atlas account or local installation)
- Docker (optional, for containerization)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/library-microservice.git
   cd library-microservice

Set up environment variables
bashcp .env.example .env
# Edit .env with your MongoDB connection details

Install dependencies
bashpip install -r requirements.txt

Configure your .env file
envMONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=library_db
ENVIRONMENT=development

Run the application
bashpython -m app.main


The API will be available at http://localhost:8000
Using Docker

Build and run with Docker Compose
bashdocker-compose up -d

Access the application

API: http://localhost:8000
Documentation: http://localhost:8000/docs



📚 API Documentation
Base URL
http://localhost:8000/api
Endpoints
Books

GET /api/books - Get all books
POST /api/books - Create a new book
GET /api/books/{id} - Get book by ID
PUT /api/books/{id} - Update book
DELETE /api/books/{id} - Delete book

Authors

GET /api/authors - Get all authors
POST /api/authors - Create a new author
GET /api/authors/{id} - Get author by ID
PUT /api/authors/{id} - Update author
DELETE /api/authors/{id} - Delete author

Categories

GET /api/categories - Get all categories
POST /api/categories - Create a new category
GET /api/categories/{id} - Get category by ID
PUT /api/categories/{id} - Update category
DELETE /api/categories/{id} - Delete category

Interactive Documentation
Visit http://localhost:8000/docs for the automatically generated Swagger UI documentation.
🔧 Configuration
Environment Variables
VariableDescriptionDefaultMONGO_URIMongoDB connection stringmongodb://localhost:27017MONGO_DB_NAMEDatabase namelibrary_dbENVIRONMENTApplication environmentdevelopmentLOG_LEVELLogging levelINFO
Database Setup
This microservice uses MongoDB. You can use:

MongoDB Atlas (recommended for production)
Local MongoDB installation
Docker MongoDB container (included in docker-compose.yml)

🧪 Testing
bash# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
🚀 Deployment
Docker Deployment
bash# Build the image
docker build -t library-microservice .

# Run the container
docker run -p 8000:8000 --env-file .env library-microservice
Production Considerations

Set ENVIRONMENT=production in your .env
Use a production WSGI server like Gunicorn
Implement proper logging and monitoring
Set up database backups
Configure HTTPS/SSL
Implement rate limiting for APIs

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🔗 Related Resources

FastAPI Documentation
MongoDB Documentation
Beanie ODM Documentation
Pydantic Documentation

📞 Support
If you have any questions or need help, please open an issue on GitHub.