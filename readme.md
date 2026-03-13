# Weather Forecasting Calculator

A personal Python project exploring weather data analysis and ML forecasting — built around an async data pipeline with a modular structure that lets me swap in different problem types as the project evolves.

## What is this?

`Calculator.py` is the main entry point. It pulls in and cleans weather station data asynchronously, then routes to one of four analysis modes depending on what I'm working on:

| Problem Type | Description | Status |
|---|---|---|
| `PROB01` | Feature analysis — correlation, uncertainty quantification, feature importance | 🔧 In progress |
| `PROB02` | Geospatial modeling — 2D/3D spatial interpolation across station grid | 🗂 Planned |
| `PROB03` | Time series forecasting — classical and ML-based approaches | 🗂 Planned |
| `PROB04` | Further ML/AI frameworks as the project matures | 🗂 Planned |

To switch between them, just change one line in `Calculator.py`:

```python
inputData["problemType"] = "PROB01"  # swap to PROB02, PROB03, or PROB04
```

## Project Structure

```
Weather-Forcasting/
├── .devcontainer/                  # VS Code dev container config
├── .github/workflows/              # GitHub Actions CI/CD
├── weatherForcastingCalculator/
│   ├── utils/
│   │   ├── dataPrepAndParser.py    # async data ingestion + cleaning
│   │   └── utils.py                # input file helpers
│   └── Data/                       # local weather data files (CSV/JSON)
├── tests/
│   └── test_calculator.py
├── Calculator.py                   # main entry point
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Getting Started

You've got three options depending on your setup.

### VS Code Dev Container (easiest)

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting
code .
```

Hit `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`, wait for the build, then:

```bash
python Calculator.py
```

Everything is pre-installed inside the container — Python 3.11, all dependencies, Black, flake8, Jupyter.

### Docker Compose

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting
docker-compose up weather-app-dev
docker-compose exec weather-app-dev bash
python Calculator.py
```

### Local Python

```bash
git clone git@github.com:tomskija/Weather-Forcasting.git
cd Weather-Forcasting
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # add your API keys
python Calculator.py
```

## Dependencies

Everything installs automatically from `requirements.txt`. Main ones worth knowing:

| Package | Purpose |
|---|---|
| `numpy` / `pandas` | Data manipulation |
| `matplotlib` / `seaborn` | Visualization |
| `scikit-learn` | ML modeling |
| `metpy` / `xarray` | Meteorological and N-dimensional data |
| `fastapi` / `aiohttp` | API layer + async HTTP |

## Problem Types

**PROB01 — Feature Analysis**
Statistical summaries and diagnostic plots for the cleaned station data — correlation matrices, uncertainty estimates, feature importance rankings.

**PROB02 — Geospatial Modeling**
Spatially interpolates weather observations across the station grid to build 2D/3D field representations for predicting conditions at unobserved locations and times.

**PROB03 — Time Series Forecasting**
ML-based prediction of weather variables forward in time, from classical approaches (ARIMA, exponential smoothing) through tree-based and neural forecasters.

**PROB04 — Additional AI/ML Frameworks**
TBD — reserved for more advanced techniques once the earlier problem types are built out.

## Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
ENV=development
DEBUG=true
PORT=8000

OPENWEATHER_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here

MODEL_TRAINING_INTERVAL_HOURS=24
PREDICTION_WINDOW_DAYS=7
```

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=weatherForcastingCalculator --cov-report=html
flake8 weatherForcastingCalculator/
black --check weatherForcastingCalculator/
```

## Deployment

```bash
# Standalone Docker
docker build -t weather-app .
docker run -p 8000:8000 weather-app

# Docker Compose
docker-compose up -d weather-app
```

CI/CD is set up via GitHub Actions — runs tests on every push, builds and pushes the Docker image to GitHub Container Registry on merges to `main`.

## Troubleshooting

**Dev container won't start** — `docker system prune -a`, then rebuild via `Ctrl+Shift+P`

**Port in use** — `lsof -i :8000` (Mac/Linux) or `netstat -ano | findstr :8000` (Windows), then kill the process or change `PORT` in `.env`

**Import errors** — check `echo $PYTHONPATH`, should be `/workspace` or `/app`

**Docker build fails** — `docker builder prune` then `docker build --no-cache -t weather-app .`

## Questions / Issues

Open an issue [here](https://github.com/tomskija/Weather-Forcasting/issues).
