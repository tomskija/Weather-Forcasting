# Weather Forecasting Calculator

A Python-based weather forecasting pipeline built around an async data ingestion and processing architecture, with a modular problem-type framework designed to support progressively advanced ML approaches — from exploratory feature analysis up to other ML/AI frameworks that bring in insights to the current project.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Problem Types](#problem-types)
- [Testing](#testing)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Overview

The core entry point is `Calculator.py`, which runs an async pipeline that ingests and cleans weather station data, then routes to one of four problem types depending on the analysis goal:

| Problem Type | Description | Status |
|---|---|---|
| `PROB01` | Feature analysis — correlation, uncertainty quantification, feature importance | 🔧 In progress |
| `PROB02` | Geospatial modeling — 2D/3D spatial interpolation across station grid | 🗂 Planned |
| `PROB03` | Time series forecasting — classical and ML-based approaches | 🗂 Planned |
| `PROB04` | Further ML/AI frameworks to draw insights into the current project | 🗂 Planned |

The pipeline is async end-to-end using Python's `asyncio`, keeping the architecture non-blocking and ready to scale to larger datasets or concurrent workloads.

## Project Structure

```
Weather-Forcasting/
├── .devcontainer/                  # VS Code dev container configuration
│   ├── devcontainer.json           # Dev container settings
│   └── Dockerfile                  # Development environment image
├── .github/workflows/              # GitHub Actions CI/CD
│   └── ci-cd.yml                   # Build, test, and deploy pipeline
├── weatherForcastingCalculator/    # Core application package
│   ├── utils/
│   │   ├── dataPrepAndParser.py    # Async data ingestion and cleaning
│   │   └── utils.py                # Input file config helpers
│   └── Data/                       # Local weather data files (CSV/JSON)
├── tests/
│   └── test_calculator.py          # Unit tests
├── Calculator.py                   # Main async pipeline entry point
├── .env.example                    # Environment variable template
├── .dockerignore
├── .gitignore
├── docker-compose.yml              # Multi-environment orchestration
├── Dockerfile                      # Production container
├── requirements.txt                # Python dependencies
└── README.md
```

## Prerequisites

### Required Software
- **Python 3.11** — [python.org](https://www.python.org/downloads/)
- **Docker Desktop** (v4.0+) — for containerized development
  - [Windows](https://docs.docker.com/desktop/windows/install/) · [macOS](https://docs.docker.com/desktop/mac/install/) · [Linux](https://docs.docker.com/desktop/linux/install/)
- **Git** (v2.30+) — [git-scm.com](https://git-scm.com/downloads)
- **VS Code** (optional but recommended) — [code.visualstudio.com](https://code.visualstudio.com/)

### VS Code Extensions (Recommended)
- **Dev Containers** (`ms-vscode-remote.remote-containers`)
- **Python** (`ms-python.python`)
- **Jupyter** (`ms-toolsai.jupyter`)
- **Docker** (`ms-azuretools.vscode-docker`)

### Core Python Dependencies
Installed automatically via `requirements.txt`:

| Package | Version | Purpose |
|---|---|---|
| `numpy` | 1.24.3 | Numerical computing and array operations |
| `pandas` | 2.0.3 | Data manipulation and analysis |
| `matplotlib` | 3.7.2 | Plotting and visualization |
| `seaborn` | 0.12.2 | Statistical data visualization |
| `scikit-learn` | 1.3.0 | ML modeling and evaluation |
| `metpy` | 1.5.1 | Meteorological data analysis |
| `xarray` | 2023.7.0 | N-dimensional labeled array support |
| `fastapi` | 0.101.1 | API layer for serving predictions |
| `aiohttp` | 3.8.5 | Async HTTP for external weather APIs |
| `requests` | 2.31.0 | HTTP client for API calls |
| `beautifulsoup4` | 4.12.2 | HTML/XML parsing for data scraping |

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB for Docker images
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+

## Quick Start

### Option 1: VS Code Dev Container (Recommended)

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting
code .
```

Then: `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`

Once the container builds:

```bash
python --version   # Should show Python 3.11.x
python Calculator.py
```

### Option 2: Docker Compose

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting

# Start dev environment
docker-compose up weather-app-dev

# Shell into the container
docker-compose exec weather-app-dev bash
python Calculator.py
```

### Option 3: Local Python Environment

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env          # Configure API keys
python Calculator.py
```

## Development Setup

### Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Application
ENV=development
DEBUG=true
PORT=8000

# Weather API Keys
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
WEATHER_API_KEY=your_weatherapi_key_here

# ML Settings
MODEL_TRAINING_INTERVAL_HOURS=24
PREDICTION_WINDOW_DAYS=7
```

### VS Code Dev Container Features

The dev container provides out of the box:
- Python 3.11 with all dependencies pre-installed
- Black (formatting) and flake8 (linting) on save
- Jupyter notebook support with port forwarding (8888)
- Breakpoint debugging
- Git + SSH key forwarding
- Non-root user setup

### Development Workflow

1. Code changes sync automatically between host and container
2. To add a dependency: update `requirements.txt` and rebuild the container
3. To modify the container environment: edit `.devcontainer/devcontainer.json`
4. Run tests with `pytest` directly in the container terminal

### Switching Problem Types

The active analysis is controlled by `problemType` in `Calculator.py`:

```python
inputData["problemType"] = "PROB01"  # Change to PROB02, PROB03, or PROB04
```

## Problem Types

### PROB01 — Feature Analysis
Generates statistical summaries and diagnostic plots for the cleaned weather station data. Planned outputs include correlation matrices, uncertainty estimates, and feature importance rankings to guide downstream modeling decisions.

### PROB02 — Geospatial Modeling
Spatially interpolates weather observations across the station grid to produce 2D/3D field representations for predicting conditions at unobserved locations and times.

### PROB03 — Time Series Forecasting
Applies ML-based approaches to predict weather variables forward in time, spanning classical methods (ARIMA, exponential smoothing) through tree-based and neural forecasters.

### PROB04 — Additional AI/ML Frameworks
Reserved for more advanced modeling techniques to be determined as the project matures.

## Production Deployment

### Docker (Standalone)

```bash
docker build -t weather-app .
docker run -p 8000:8000 weather-app
```

### Docker Compose

```bash
# Foreground
docker-compose up weather-app

# Background
docker-compose up -d weather-app
```

### Kubernetes (Advanced)

```yaml
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

### GitHub Actions CI/CD

The included workflow automatically:
1. Runs tests on every push and PR
2. Builds and tags the Docker image on merges to `main`
3. Pushes to GitHub Container Registry

To enable: go to Settings → Secrets and ensure `GITHUB_TOKEN` has package write permissions.

## Testing

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=weatherForcastingCalculator --cov-report=html

# Targeted
pytest tests/ -k "test_data" -v     # Data pipeline tests
pytest tests/ -k "test_model" -v    # ML model tests
pytest tests/ -k "test_api" -v      # API endpoint tests

# Code quality
flake8 weatherForcastingCalculator/
black --check weatherForcastingCalculator/
```

Coverage reports are written to `htmlcov/` after running with the `--cov-report=html` flag.

## Contributing

1. Fork and clone the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Set up the dev environment (Dev Container or local venv)
4. Make changes, add tests, update docs
5. Run `pytest` and linting checks before committing
6. Open a PR with a clear description

### Commit Convention

This project uses [Conventional Commits](https://conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code restructure, no behavior change
- `test:` — test additions or updates
- `chore:` — build / tooling changes

## Troubleshooting

**Dev container won't start**
```bash
docker system prune -a
# Then: Ctrl+Shift+P → Dev Containers: Rebuild Container
```

**Port already in use**
```bash
lsof -i :8000                 # macOS/Linux
netstat -ano | findstr :8000  # Windows
# Kill the process or change PORT in .env
```

**Python import errors**
```bash
echo $PYTHONPATH   # Should be /workspace or /app
ls -la weatherForcastingCalculator/
```

**Docker build fails**
```bash
docker builder prune
docker build --no-cache -t weather-app .
```

**Slow container builds**
- Increase Docker memory to 8GB in Docker Desktop settings
- Enable Docker Compose V2
- Verify `.dockerignore` excludes `Data/`, `venv/`, `htmlcov/`

## Support

- **Bugs / feature requests**: [Open an issue](https://github.com/tomskija/Weather-Forcasting/issues)
- **Docker docs**: [docs.docker.com](https://docs.docker.com/)
- **VS Code docs**: [code.visualstudio.com/docs](https://code.visualstudio.com/docs)
