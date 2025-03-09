# GitHub Stats API

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mrwhoknows55/github-fastapi.git
   cd github-fastapi
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API

Run the FastAPI application using uvicorn:

```bash
uvicorn src.main:app --reload
```

or using Docker compose:

```bash
docker compose up
```


The API will be available at http://localhost:8000
The swagger documentation at http://localhost:8000/docs