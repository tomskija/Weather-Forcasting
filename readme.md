# Weather Forecasting Calculator

A Python-based weather forecasting application with containerized development and production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Database Setup (Optional)](#database-setup-optional)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- **Docker Desktop** (v4.0+)
  - [Download for Windows](https://docs.docker.com/desktop/windows/install/)
  - [Download for macOS](https://docs.docker.com/desktop/mac/install/)
  - [Download for Linux](https://docs.docker.com/desktop/linux/install/)
- **Visual Studio Code** (latest version)
  - [Download here](https://code.visualstudio.com/)
- **Git** (v2.30+)
  - [Download here](https://git-scm.com/downloads)

### Required VS Code Extensions
- **Dev Containers** (ms-vscode-remote.remote-containers)
- **Python** (ms-python.python)
- **Docker** (ms-azuretools.vscode-docker)
- **Jupyter** (ms-toolsai.jupyter) - for data analysis notebooks

### Core Python Dependencies
The project includes these main libraries (automatically installed):
- **numpy** (1.24.3) - Numerical computing
- **pandas** (2.0.3) - Data manipulation and analysis
- **matplotlib** (3.7.2) - Plotting and visualization
- **seaborn** (0.12.2) - Statistical data visualization
- **scikit-learn** (1.3.0) - Machine learning library
- **beautifulsoup4** (4.12.2) - Web scraping and HTML parsing
- **requests** (2.31.0) - HTTP library for API calls

### Optional Database Dependencies
If using database features, these will be installed:
- **psycopg2-binary** (2.9.7) - PostgreSQL adapter
- **SQLAlchemy** (2.0.21) - Database ORM
- **redis** (5.0.1) - In-memory caching

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space for Docker images
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+

## Quick Start

### Option 1: Development with VS Code Dev Containers (Recommended)

1. **Clone the repository**
   ```bash
   git clone git@github.com:tomskija/Weather-Forcasting.git
   cd Weather-Forcasting
   ```

2. **Open in VS Code**
   ```bash
   code .
   ```

3. **Start Dev Container**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: `Dev Containers: Reopen in Container`
   - Select the command and wait for the container to build

4. **Verify Setup**
   ```bash
   python --version  # Should show Python 3.11.x
   pip list          # Should show installed packages
   ```

5. **Run the Application**
   ```bash
   python weatherForcastingCalculator/Calculator.py
   ```

### Option 2: Local Development with Docker Compose

1. **Clone the repository**
   ```bash
   git clone git@github.com:tomskija/Weather-Forcasting.git
   cd Weather-Forcasting
   ```

2. **Start Development Environment (File-based)**
   ```bash
   docker-compose up weather-app-dev
   ```

3. **Start Development Environment (With Database)**
   ```bash
   # Include PostgreSQL database
   docker-compose up postgres weather-app-dev
   ```

4. **Access the container**
   ```bash
   docker-compose exec weather-app-dev bash
   ```

### Option 3: Traditional Python Setup

1. **Install Python 3.11**
   - [Download from python.org](https://www.python.org/downloads/)

2. **Clone and Setup**
   ```bash
   git clone git@github.com:tomskija/Weather-Forcasting.git
   cd Weather-Forcasting
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Optional: Enable Database Features**
   ```bash
   # If you want database support, uncomment database lines in requirements.txt and reinstall:
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python weatherForcastingCalculator/Calculator.py
   ```

## Development Setup

### Environment Configuration

1. **Create environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values**
   ```bash
   # Open .env and configure:
   ENV=development
   DEBUG=true
   PORT=8000
   
   # Database (optional - only if using database features)
   # DATABASE_URL=postgresql://weather_user:weather_pass@localhost:5432/weather_forecast_db
   ```

### VS Code Dev Container Features

The dev container automatically provides:
- Python 3.11 with all dependencies
- Pre-configured VS Code extensions
- Debugging capabilities
- Port forwarding (8000, 5000)
- Git integration
- Non-root user setup for security

### Making Changes

1. **Code changes** are automatically synced between host and container
2. **Dependencies**: Add to `requirements.txt` and rebuild container
3. **Container changes**: Modify `.devcontainer/devcontainer.json`

## Database Setup (Optional)

The project includes optional database support for advanced weather data storage and analysis.

### When to Use Database Setup

**Use database setup if you need:**
- Historical weather data storage and analysis
- User preferences and multi-user support
- Weather alerts and notification system
- Forecast accuracy tracking
- Complex queries and reporting

**Skip database setup if you:**
- Are doing simple weather calculations
- Working with file-based data only
- Don't need persistent storage
- Want a lighter development environment

### Database Setup Instructions

1. **Install Database Dependencies (Optional)**
   
   **Option A: Enable database in requirements.txt**
   ```bash
   # Edit requirements.txt - uncomment these lines:
   psycopg2-binary==2.9.7
   SQLAlchemy==2.0.21
   alembic==1.12.0
   redis==5.0.1
   
   # Then install
   pip install -r requirements.txt
   ```
   
   **Option B: Install database packages separately**
   ```bash
   pip install psycopg2-binary==2.9.7 SQLAlchemy==2.0.21 alembic==1.12.0 redis==5.0.1
   ```

2. **Start with Database Services**
   ```bash
   # Start PostgreSQL, Redis, and your app
   docker-compose up postgres redis weather-app
   
   # For development with database
   docker-compose up postgres redis weather-app-dev
   ```

3. **Access Database Tools**
   - **pgAdmin**: http://localhost:5050
     - Email: admin@weather.com
     - Password: admin123
   - **Direct Database Connection**:
     - Host: localhost:5432
     - Database: weather_forecast_db
     - User: weather_user
     - Password: weather_pass

4. **Database Features Available**
   - Pre-built schema with weather stations, historical data, forecasts
   - Sample data for 8 US cities
   - Common queries for weather analysis
   - User preference management
   - Weather alerts system

### File-Only Setup (No Database)

If you prefer to work without a database:

```bash
# Simple app without database dependencies
docker-compose up weather-app

# Development without database
docker run -it -v $(pwd):/workspace your-weather-app bash
```

Your application will work with file-based data in the `weatherForcastingCalculator/Data/` directory.

## Production Deployment

### Simple Production (File-based)

```bash
# Build production image
docker build -t weather-app .

# Run production container
docker run -p 8000:8000 weather-app
```

### Production with Database

```bash
# Full production stack with database
docker-compose up postgres redis weather-app

# Background deployment
docker-compose up -d postgres redis weather-app
```

### Using Docker Compose

```bash
# Production deployment
docker-compose up weather-app

# Background deployment
docker-compose up -d weather-app
```

### GitHub Actions CI/CD

The project includes automated CI/CD that:
1. **Tests** code on every push/PR
2. **Builds** Docker image on main branch
3. **Pushes** to GitHub Container Registry
4. **Deploys** to production (configure deployment step)

**Setup GitHub Actions:**
1. Go to repository Settings → Secrets
2. Ensure `GITHUB_TOKEN` has package write permissions
3. Push to `main` branch to trigger deployment

## Project Structure

```
WEATHER-FORCASTING/
├── .devcontainer/              # VS Code dev container configuration
│   ├── devcontainer.json       # Dev container settings
│   └── Dockerfile             # Development environment
├── .github/workflows/         # GitHub Actions CI/CD
│   └── ci-cd.yml             # Build, test, and deploy pipeline
├── sql/                      # Database scripts (OPTIONAL)
│   ├── init_schema.sql       # Database schema creation
│   ├── seed_data.sql        # Sample data for development
│   └── common_queries.sql   # Useful queries for your app
├── weatherForcastingCalculator/ # Main application code
│   ├── Data/                 # Weather data files
│   ├── utils/                # Utility functions
│   └── Calculator.py         # Main application entry point
├── tests/                    # Test files
│   └── test_calculator.py    # Unit tests
├── .dockerignore            # Docker build exclusions
├── .env.example            # Environment variables template
├── .gitignore             # Git exclusions
├── docker-compose.yml     # Multi-environment orchestration
├── Dockerfile            # Production container
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Testing

### Run Tests in Dev Container

```bash
# In VS Code dev container terminal
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=weatherForcastingCalculator --cov-report=html
```

### Run Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes in dev container**
4. **Add tests** for new functionality
5. **Commit changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push and create pull request**

### Code Quality

The project enforces:
- **Linting**: flake8
- **Testing**: pytest with coverage
- **Formatting**: black (auto-applied in dev container)

## Troubleshooting

### Common Issues

**Dev Container Won't Start**
```bash
# Clear Docker cache
docker system prune -a
# Rebuild container
Ctrl+Shift+P → "Dev Containers: Rebuild Container"
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in .env
```

**Python Import Errors**
```bash
# Check Python path in container
echo $PYTHONPATH
# Should be /workspace or /app

# Verify file structure
ls -la weatherForcastingCalculator/
```

**Docker Build Fails**
```bash
# Check Docker is running
docker --version

# Clear build cache
docker builder prune

# Rebuild with no cache
docker build --no-cache -t weather-app .
```

### Getting Help

1. **Check logs**
   ```bash
   # Container logs
   docker-compose logs weather-app
   
   # Dev container logs
   # View through VS Code: View → Output → Dev Containers
   ```

2. **Verify setup**
   ```bash
   # Check Docker
   docker --version
   docker-compose --version
   
   # Check VS Code extensions
   code --list-extensions | grep remote-containers
   ```

3. **Reset environment**
   ```bash
   # Stop all containers
   docker-compose down
   
   # Remove volumes
   docker-compose down -v
   
   # Rebuild
   docker-compose up --build
   ```

### Performance Optimization

**Slow Container Builds**
- Enable Docker Desktop's "Use Docker Compose V2"
- Increase Docker memory allocation (8GB recommended)
- Use `.dockerignore` to exclude unnecessary files

**Slow File Sync**
- On Windows: Use WSL2 backend
- On macOS: Enable "Use gRPC FUSE for file sharing"

**Database Performance (if using database)**
- Increase PostgreSQL shared_buffers in production
- Use connection pooling for multiple connections
- Monitor query performance with pgAdmin

## Deployment Options

### Option 1: File-Based Application (Simplest)
- Works with local files in `Data/` directory
- No database setup required
- Best for: Simple calculations, prototyping, single-user scenarios

### Option 2: Database-Backed Application (Advanced)  
- PostgreSQL for structured data storage
- Redis for caching
- pgAdmin for database management
- Best for: Multi-user applications, historical analysis, production systems

## Support

For issues related to:
- **Application bugs**: Create an issue in this repository
- **Docker problems**: Check [Docker documentation](https://docs.docker.com/)
- **VS Code issues**: Check [VS Code documentation](https://code.visualstudio.com/docs)