# EOL Checker

This repository contains a small FastAPI microservice that exposes an endpoint to check whether a given software version is still supported. The service retrieves data from the public [endoflife.date](https://endoflife.date) API and caches the results locally.

## Running the service

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn eol_service.main:app --reload
```

The first request for a software pulls data from the remote API and stores it under `eol_service/cache/`. Subsequent requests use the cached files.

Query the service using:

```bash
curl 'http://localhost:8000/eol?name=ubuntu&version=22.04'
```

## Tests

Run the unit tests with:

```bash
pytest
```

## Continuous Integration

The repository provides a GitHub Actions workflow located under
`.github/workflows/python-app.yml`. This pipeline installs dependencies,
runs the unit tests and builds distribution artifacts for every push and
pull request.
