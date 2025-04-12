# IliadStats

**IliadStats** is a Python module for scraping information from the Iliad dashboard. It allows you to programmatically retrieve details such as traffic consumption, traffic endowment, and renewal dates from your Iliad account. **More to come!**

---

## Features

- **Traffic Consumption**: Retrieve the amount of data you've used.
- **Traffic Endowment**: Get the total data available in your plan.
- **Renewal Date**: Fetch the next renewal date for your plan.
- **Used Minutes**: Retrieve the amount of minutes spent in calls **(coming soon)**
- **Sent SMS**: Get the number of sent SMSs **(coming soon)**

---

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