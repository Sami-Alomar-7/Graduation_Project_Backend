# 🎓 Graduation Project - Django Backend API

A robust Django REST API backend with authentication, admin panel, customer management, and real-time notifications. Built with modern Django practices, Docker containerization, and microservices architecture.

## 🚀 Features

- **🔐 JWT Authentication** - Secure token-based authentication system
- **👥 User Management** - Custom user model with role-based permissions
- **📧 Email Integration** - Gmail API integration for automated emails
- **⚡ Real-time Notifications** - WebSocket support with Django Channels
- **🔄 Background Tasks** - Celery integration for async task processing
- **🐳 Docker Containerization** - Complete containerized deployment
- **🌐 Nginx Reverse Proxy** - Production-ready web server configuration
- **📊 Admin Panel** - Custom admin interface with advanced features
- **🔍 API Documentation** - RESTful API with comprehensive endpoints
- **🛡️ Security** - CORS, JWT blacklisting, and security best practices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (80)    │    │  Django App     │    │   PostgreSQL    │
│   (Reverse      │◄──►│   (8000/8001)   │◄──►│   Database      │
│    Proxy)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   Redis Cache   │◄─────────────┘
                        │   & Message     │
                        │     Broker      │
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │   Celery        │
                        │   Workers       │
                        └─────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- **Git** (for version control)

## 🛠️ Quick Setup for Frontend Development

### 1. Clone the Repository

```bash
git clone <https://github.com/Sami-Alomar-7/Graduation_Project_Backend>
cd Graduation_Project
```

### 2. Environment Configuration

You'll receive the required `.env` file from the backend team. Place it in the root directory of the project.

### 3. Start the Backend Services

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Verify Backend is Running

The backend will be available at:
- **API Base URL**: `http://localhost:8000`
- **Nginx Proxy**: `http://localhost:80`
- **WebSocket**: `ws://localhost:8001`

### 5. Stop Services (when needed)

```bash
# Stop all services
docker-compose down

# View logs if needed
docker-compose logs -f app
```

## 🚀 Available Services

Once running, you'll have access to:

- **Django API**: `http://localhost:8000` - Main API endpoints
- **Nginx**: `http://localhost:80` - Reverse proxy (use this for production-like testing)
- **PgAdmin**: `http://localhost:5050` - Database management (admin@example.com / admin)
- **Flower**: `http://localhost:5555` - Celery task monitoring
- **WebSocket**: `ws://localhost:8001/ws/notifications/` - Real-time notifications

## 🔧 Frontend Development Tips

1. **API Base URL**: Use `http://localhost:8000` for direct API calls or `http://localhost:80` for production-like testing
2. **CORS**: The backend is configured to accept requests from frontend development servers
3. **Authentication**: Use JWT tokens for API authentication
4. **WebSocket**: Connect to `ws://localhost:8001/ws/notifications/` for real-time features

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the ports
   docker-compose down
   # Then restart
   docker-compose up --build
   ```

2. **Build Failures**
   ```bash
   # Clear Docker cache and rebuild
   docker system prune -a
   docker-compose build --no-cache
   ```

3. **Services Not Starting**
   ```bash
   # Check logs
   docker-compose logs -f app
   docker-compose logs -f nginx
   ```

### Getting Help

If you encounter any issues:
1. Check the logs: `docker-compose logs -f [service-name]`
2. Ensure the `.env` file is properly configured
3. Contact the backend team for support