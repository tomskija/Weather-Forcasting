# Weather Forecasting Calculator

A comprehensive Python-based weather forecasting application with containerized development and production environments, featuring optional database integration and modern DevOps practices.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Database Setup (Optional)](#database-setup-optional)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [API Documentation](#api-documentation)
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
- **numpy** (1.24.3) - Numerical computing and array operations
- **pandas** (2.0.3) - Data manipulation and analysis
- **matplotlib** (3.7.2) - Plotting and visualization
- **seaborn** (0.12.2) - Statistical data visualization
- **scikit-learn** (1.3.0) - Machine learning library
- **beautifulsoup4** (4.12.2) - Web scraping and HTML parsing
- **requests** (2.31.0) - HTTP library for API calls
- **aiohttp** (3.8.5) - Async HTTP client/server framework
- **fastapi** (0.101.1) - Modern web framework for APIs
- **metpy** (1.5.1) - Weather data analysis tools
- **xarray** (2023.7.0) - N-dimensional data arrays

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
   cd WEATHER-FORCASTING
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

### Option 2: Docker Compose Development

#### Simple File-Based Development
```bash
# Clone the repository
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting

# Start development environment (file-based only)
docker-compose up weather-app-dev

# Access the container
docker-compose exec weather-app-dev bash
```

#### Development with Database (Optional)
```bash
# Start with full database stack
docker-compose --profile database up weather-app-dev-db

# Or start individual services
docker-compose up postgres redis weather-app-dev
```

#### Production Deployment via Docker Compose
```bash
# Simple production (file-based)
docker-compose up weather-app

# Production with database
docker-compose --profile database up weather-app-db

# Full stack deployment
docker-compose --profile full up
```

### Option 3: Traditional Python Setup

1. **Install Python 3.11**
   - [Download from python.org](https://www.python.org/downloads/)

2. **Clone and Setup Virtual Environment**
   ```bash
   git clone git@github.com:tomskija/Weather-Forcasting.git
   cd Weather-Forcasting
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and preferences
   ```

4. **Optional: Enable Database Features**
   ```bash
   # Uncomment database dependencies in requirements.txt, then:
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python weatherForcastingCalculator/Calculator.py
   ```

## Advanced Usage

### Environment Profiles
The application supports multiple environment profiles via Docker Compose:

```bash
# Default (no profile) - Basic file-based services
docker-compose up

# Database profile - Includes PostgreSQL, Redis, pgAdmin
docker-compose --profile database up

# Full profile - All services including monitoring
docker-compose --profile full up
```

### Service Variants
| Service | Port | Purpose | Database |
|---------|------|---------|----------|
| `weather-app` | 8000 | Production (file-based) | ❌ |
| `weather-app-db` | 8001 | Production (with database) | ✅ |
| `weather-app-dev` | 8002 | Development (file-based) | ❌ |
| `weather-app-dev-db` | 8003 | Development (with database) | ✅ |

### API Access
When running, the application provides:
- **Main API**: http://localhost:8000 (or respective port)
- **Database Admin**: http://localhost:5050 (pgAdmin)
- **Health Check**: http://localhost:8000/health

## Development Setup

### Environment Configuration

1. **Create environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values**
   ```bash
   # Application settings
   ENV=development
   DEBUG=true
   PORT=8000
   
   # Weather API Keys (get from respective providers)
   OPENWEATHER_API_KEY=your_openweathermap_api_key_here
   WEATHER_API_KEY=your_weatherapi_key_here
   
   # Database (optional - only if using database features)
   DATABASE_URL=postgresql://weather_user:weather_pass@localhost:5432/weather_forecast_db
   REDIS_URL=redis://localhost:6379/0
   
   # Machine Learning Settings
   MODEL_TRAINING_INTERVAL_HOURS=24
   PREDICTION_WINDOW_DAYS=7
   ```

### VS Code Dev Container Features

The dev container automatically provides:
- Python 3.11 with all dependencies pre-installed
- Pre-configured VS Code extensions for Python, Docker, and Jupyter
- Code formatting (Black) and linting (flake8) on save
- Debugging capabilities with breakpoint support
- Port forwarding (8000, 5000, 8888 for Jupyter)
- Git integration with SSH key forwarding
- Non-root user setup for security
- Automatic environment variable loading

### Development Workflow

1. **Code changes** are automatically synced between host and container
2. **Dependencies**: Add to `requirements.txt` and rebuild container  
3. **Container changes**: Modify `.devcontainer/devcontainer.json`
4. **Database changes**: Update SQL scripts in `sql/` directory
5. **Testing**: Run `pytest` directly in the container terminal

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

2. **Start Database Services**
   ```bash
   # Using Docker Compose profiles
   docker-compose --profile database up
   
   # Or start specific services
   docker-compose up postgres redis pgadmin
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
   - **Redis**: localhost:6379

4. **Database Features Available**
   - Pre-built schema with weather stations, historical data, forecasts
   - Sample data for 8 US cities with realistic weather patterns
   - Common queries for weather analysis and reporting
   - User preference management system
   - Weather alerts and notification system
   - Forecast accuracy tracking and model performance metrics

### Database Schema Overview

The database includes these main tables:
- `weather_stations` - Global weather station registry
- `weather_data` - Historical weather observations
- `weather_forecasts` - Prediction data with confidence scores
- `forecast_accuracy` - Model performance tracking
- `weather_alerts` - Alert and notification management
- `user_preferences` - Multi-user configuration support

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
# Build and run production image
docker build -t weather-app .
docker run -p 8000:8000 weather-app
```

### Production with Docker Compose

```bash
# File-based production deployment
docker-compose up weather-app

# Full production stack with database
docker-compose --profile database up weather-app-db

# Background deployment
docker-compose --profile database up -d weather-app-db
```

### Kubernetes Deployment (Advanced)

```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weather-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: weather-app
  template:
    metadata:
      labels:
        app: weather-app
    spec:
      containers:
      - name: weather-app
        image: ghcr.io/tomskija/weather-forcasting:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: "production"
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

### Key Directories Explained

**`weatherForcastingCalculator/`** - Core application logic
- `Calculator.py` - Main weather calculation engine
- `utils/` - Helper functions for data processing
- `Data/` - Local weather data files (CSV, JSON formats)

**`.devcontainer/`** - Development environment configuration  
- Enables instant development setup with VS Code
- Pre-configured with Python, extensions, and debugging

**`sql/`** - Database infrastructure (optional)
- Complete schema for weather data storage
- Sample data for testing and development
- Optimized queries for common operations

**`tests/`** - Automated testing suite
- Unit tests with pytest framework  
- Coverage reporting and quality metrics
- Integration tests for database operations

## Testing

### Running Tests in Development Container

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage reporting  
pytest tests/ --cov=weatherForcastingCalculator --cov-report=html

# Run specific test categories
pytest tests/ -k "test_data" -v          # Data processing tests
pytest tests/ -k "test_model" -v         # ML model tests  
pytest tests/ -k "test_api" -v           # API endpoint tests
```

### Local Testing (Traditional Python)

```bash
# Install test dependencies
pip install pytest pytest-cov flake8 black

# Run tests
pytest tests/

# Run with coverage
pytest --cov=weatherForcastingCalculator --cov-report=term-missing

# Code quality checks
flake8 weatherForcastingCalculator/
black --check weatherForcastingCalculator/
```

### Test Categories

The test suite covers:

**Unit Tests** (`test_calculator.py`)
- Core weather calculation functions
- Data validation and processing
- Error handling and edge cases

**Integration Tests** (when database enabled)
- Database connection and queries
- API endpoint functionality  
- File I/O operations

**Performance Tests**
- Large dataset processing
- Model prediction speed
- API response times

### Continuous Testing

Tests automatically run on:
- Every commit push
- Pull request creation
- Scheduled runs (daily)
- Before production deployments

Coverage reports are generated and can be viewed in the `htmlcov/` directory after running tests.

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork and Clone**
   ```bash
   git clone git@github.com:YOUR-USERNAME/Weather-Forcasting.git
   cd Weather-Forcasting
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   # Option 1: Use Dev Container (Recommended)
   code .  # Open in VS Code, then reopen in container
   
   # Option 2: Local Setup
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Make Changes**
   - Write your code following existing patterns
   - Add tests for new functionality
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code quality
   flake8 weatherForcastingCalculator/
   black weatherForcastingCalculator/
   
   # Test different configurations
   docker-compose up weather-app-dev  # Test file-based mode
   docker-compose --profile database up weather-app-dev-db  # Test with database
   ```

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add weather prediction feature"  # Use conventional commits
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all CI checks pass

### Code Quality Standards

The project enforces:
- **Linting**: flake8 for code standards
- **Formatting**: black for consistent code style  
- **Testing**: pytest with minimum 80% coverage
- **Documentation**: Clear docstrings and comments
- **Type Hints**: Use Python type annotations where applicable

### Commit Convention

We use [Conventional Commits](https://conventionalcommits.org/):
- `feat:` - New features
- `fix:` - Bug fixes  
- `docs:` - Documentation updates
- `style:` - Code formatting changes
- `refactor:` - Code refactoring
- `test:` - Test additions or updates
- `chore:` - Build process or auxiliary tool changes

## API Documentation

### Weather Endpoints

When running the application, the following endpoints are available:

```bash
# Health check
GET /health

# Current weather data
GET /weather/current?location={city_name}

# Weather forecast  
GET /weather/forecast?location={city_name}&days={1-7}

# Historical weather data
GET /weather/history?location={city_name}&date={YYYY-MM-DD}

# Weather alerts
GET /weather/alerts?location={city_name}
```

### Example API Usage

```python
import requests

# Get current weather
response = requests.get('http://localhost:8000/weather/current?location=New York')
weather_data = response.json()

# Get 5-day forecast
forecast = requests.get('http://localhost:8000/weather/forecast?location=New York&days=5')
forecast_data = forecast.json()
```

### Response Format

```json
{
  "location": {
    "city": "New York",
    "country": "US",
    "coordinates": [40.7128, -74.0060]
  },
  "current": {
    "temperature": 22.5,
    "humidity": 65,
    "pressure": 1013.25,
    "wind_speed": 3.2,
    "conditions": "partly cloudy"
  },
  "forecast": [
    {
      "date": "2025-08-29",
      "high": 26,
      "low": 18,
      "conditions": "sunny",
      "precipitation_chance": 10
    }
  ]
}
```

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