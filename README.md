# IliadStats

**IliadStats** is a Python module for scraping information from the Iliad dashboard. It allows you to programmatically retrieve details such as traffic consumption, traffic endowment, and renewal dates from your Iliad account. **More to come!**

## Features

- **Traffic Consumption**: Retrieve the amount of data you've used.
- **Traffic Endowment**: Get the total data available in your plan.
- **Renewal Date**: Fetch the next renewal date for your plan.
- **Used Minutes**: Retrieve the amount of minutes spent in calls **(coming soon)**
- **Sent SMS**: Get the number of sent SMSs **(coming soon)**

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/EugenioMoro/iliadstats.git
   cd iliadstats
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Secrets file
Before using the module, you need to create a `secrets.json` file containing your Iliad account credentials. 

Example `secrets.json`:
```json
{
    "username": "your_username",
    "password": "your_password",
    "token": ""
}
```
Token can be left empty, as it will be fetched automatically at the first login and refreshed when needed. 

### Running the example
An example script (`example.py`) is included in the repository to demonstrate how to use the module.

Before running the example, make sure to create the secrets file and specify its path in the example.

## FastAPI Deployment

The IliadStats module can also be deployed as a RESTful API using FastAPI. This allows you to expose the module's functionality via HTTP endpoints.

---

### Running the FastAPI Server

1. Ensure you have installed the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn api-server:app --reload
   ```

   By default, the server will run at `http://127.0.0.1:8000`.

---

### Running the FastAPI Server with Docker Compose

You can run the FastAPI server using Docker Compose with the prebuilt image.

1. Ensure you have a `secrets.json` file in the root of your project directory.

2. Use the following docker compose file, or download `docker-compose.yml` from this repo:
```yaml
services:
  iliadstats:
    image: ghcr.io/EugenioMoro/iliadstats:latest
    ports:
      - "8000:8000"
    volumes:
      - ./secrets.json:/app/secrets.json
    environment:
      - PYTHONUNBUFFERED=1
```


2. Start the container:
   ```bash
   docker compose up
   ```

3. Access the server at `http://127.0.0.1:8000`.

### API Endpoints

- **GET `/api/v1/used-data`**: Fetch the amount of data used.
- **GET `/api/v1/traffic-endowment`**: Fetch the total data available in your plan.
- **GET `/api/v1/renewal-date`**: Fetch the next renewal date for your plan.

---

### Interactive API Documentation

FastAPI provides interactive documentation for the API:

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs`
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc`

These interfaces allow you to test the API endpoints directly from your browser.

## API Reference

`IliadStats` Class

### Initialization:
```python
ilistats = IliadStats(secrets_file_path="path/to/secrets.json", refresh_interval=120)
```
* `secrets_file_path`: Path to the secrets.json file.
* `refresh_interval`: Time in seconds to wait before refreshing the dashboard (default: 120 seconds).

### Methods:

* `get_traffic_consumption()`: Returns the amount of data used (in GB).
* `get_traffic_endowment()`: Returns the total data available (in GB).
* `get_renewal_date()`: Returns the next renewal date as a `time.struct_time` object.

## Development

### Tests
Tests for this module are currently a **WIP**. Once completed, they will ensure the reliability of the module and cover edge cases.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the module.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer
This module is not affiliated with or endorsed by Iliad. Use it at your own risk.