### README.md

```markdown
# HydrogenFactory

API for controlling a hydrogen production factory, enabling configuration of electrolyzers and storage, and optimizing production schedules using linear programming.

## Basic Idea

The HydrogenFactory API allows users to:
- Configure **electrolyzers** (PEM or Alkaline) with specified power capacity and efficiency.
- Configure **storage** with maximum hydrogen capacity.
- Optimize a 24-hour **production schedule** to minimize electricity costs, using random or user-provided electricity prices and hydrogen demand, with configurations stored in `config.json`.

The API uses FastAPI for a robust, asynchronous interface and PuLP for linear optimization, ensuring efficient hydrogen production planning.

## How to Run the API

1. **Install Poetry**:
   Ensure Poetry is installed:
   ```bash
   pip install poetry
   ```

2. **Install Dependencies**:
   Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

3. **Run the API**:
   Start the FastAPI application with Uvicorn:
   ```bash
   poetry run uvicorn hydrogen_factory.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - `--reload` enables auto-restart on code changes (development mode).
   - The API will be available at `http://localhost:8000`.

4. **Access the API**:
   - **Root Endpoint**: Visit `http://localhost:8000/` to see the welcome message.
   - **Interactive Docs**: Open `http://localhost:8000/docs` for a Swagger UI to explore and test endpoints.

## How to Test the API

The API includes three main endpoints, which can be tested using the Swagger UI (`http://localhost:8000/docs`) or `curl`.

### Endpoints
1. **POST /api/electrolyzer/configure**
   - Configures an electrolyzer.
   - Example:
     ```bash
     curl -X POST "http://localhost:8000/api/electrolyzer/configure" -H "Content-Type: application/json" -d '{"electrolyzer_id": "E1", "type": "PEM", "capacity": 1000.0, "efficiency": 0.02}'
     ```

2. **POST /api/storage/configure**
   - Configures storage.
   - Example:
     ```bash
     curl -X POST "http://localhost:8000/api/storage/configure" -H "Content-Type: application/json" -d '{"storage_id": "S1", "max_capacity": 100.0}'
     ```

3. **POST /api/schedule/optimize**
   - Optimizes the production schedule for 24 hours.
   - Example:
     ```bash
     curl -X POST "http://localhost:8000/api/schedule/optimize" -H "Content-Type: application/json" -d '{"electrolyzer_id": "E1", "storage_id": "S1"}'
     ```

### Running Automated Tests
The project includes unit and integration tests in `tests/`.
- Run all tests:
  ```bash
  poetry run pytest tests/ -v
  ```
- Run API tests specifically:
  ```bash
  poetry run pytest tests/test_api/ -v
  ```

