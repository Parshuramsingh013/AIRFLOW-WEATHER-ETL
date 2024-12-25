# Multi-Location Weather ETL with Apache Airflow

This Airflow project is designed to extract, transform, and load (ETL) weather data from an external weather API for multiple locations into a PostgreSQL database. 

## Project Structure

```
├── dags/
│   ├── exampledag.py
│   ├── firstdag.py
│   └── multi_location_weather_etl.py   # The main DAG file
├── tests/
│   ├── dags/
│   │   └── test_dag_example.py
├── .astro/
│   ├── config.yaml
├── airflow_settings.yaml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md                           # This file
```

## Prerequisites

1. **Airflow Setup**: Ensure you have Airflow installed and configured in your environment. If using Docker, include the `docker-compose.yml` file in your setup.

2. **API Access**: Create an Airflow HTTP connection (`open_mateo_api`) for the weather API in the Airflow Admin Connections UI. Provide the base URL and API Key.

3. **PostgreSQL Setup**: Create a PostgreSQL database and set up a connection in Airflow (`postgres_default`).

4. **Python Requirements**: Install the required Python libraries using `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

## DAG Details

### **DAG ID**: `multi_location_weather_etl`

### Description

This DAG performs the following steps:

1. **Extract Weather Data**: Fetches weather data for multiple locations using the Open-Meteo API.
2. **Transform Weather Data**: Cleans and structures the data for database insertion.
3. **Load Weather Data**: Inserts the transformed data into a PostgreSQL table.

### Tasks

#### 1. `extract_weather_data()`
- Fetches weather data for specified locations using the Open-Meteo API.
- Uses an Airflow HTTP Hook for API communication.

#### 2. `transform_weather_data(weather_data_list)`
- Processes raw weather data and extracts relevant fields.
- Structures the data for insertion into PostgreSQL.

#### 3. `load_weather_data(transformed_data_list)`
- Creates a table (`weather_data`) if it doesn't exist.
- Inserts the processed weather data into the table.

### Key Variables
- **`LOCATIONS`**: List of geographic coordinates for fetching weather data.
- **`API_CONN_ID`**: Airflow connection ID for the weather API.
- **`POSTGRES_CONN_ID`**: Airflow connection ID for PostgreSQL.

## Setup Instructions

1. **Configure Airflow Connections**:
   - Set up `open_mateo_api` for the weather API.
   - Set up `postgres_default` for the PostgreSQL database.

2. **Enable the DAG**:
   - Copy the DAG file (`multi_location_weather_etl.py`) into the `dags` folder of your Airflow project.
   - Start the Airflow webserver and scheduler.
   - Enable the DAG from the Airflow UI.

3. **Run the DAG**:
   - Trigger the DAG manually or set it to run on the predefined schedule (`@daily`).

## Example PostgreSQL Table

The weather data is stored in the `weather_data` table with the following schema:

| Column        | Type     | Description                      |
|---------------|----------|----------------------------------|
| latitude      | FLOAT    | Latitude of the location         |
| longitude     | FLOAT    | Longitude of the location        |
| temperature   | FLOAT    | Current temperature              |
| windspeed     | FLOAT    | Current wind speed               |
| winddirection | FLOAT    | Direction of the wind (degrees)  |
| weathercode   | FLOAT    | Weather condition code           |
| timestamp     | TIMESTAMP| Record creation timestamp        |

## Dependencies

- **Airflow Providers**:
  - `apache-airflow-providers-http`
  - `apache-airflow-providers-postgres`
- **PostgreSQL**

## Running with Docker

To set up the project using Docker:

1. Build the Docker image:

   ```bash
   docker-compose build
   ```

2. Start the containers:

   ```bash
   docker-compose up
   ```

## Contributions

Feel free to contribute by submitting pull requests or reporting issues.

## License

This project is open-source and available under the [MIT License](LICENSE).
