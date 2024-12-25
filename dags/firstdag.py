from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import json


LOCATIONS = [
    {'latitude': '37.7749', 'longitude': '-122.4194'},
    {'latitude': '40.7128', 'longitude': '-74.0060'},
    {'latitude': '41.8781', 'longitude': '-87.6298'},
    {'latitude': '34.0522', 'longitude': '-118.2437'}
]

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_mateo_api'

default_args = {
    'owner' : 'airflow',
    'start_date' : days_ago(0),
    'retries' :1 
}

with DAG (
    dag_id = 'multi_location_weather_etl',
    default_args= default_args,
    schedule_interval="@daily",
    catchup=False
)as dag:
    

    @task()
    def extract_weather_data():
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        weather_data_list = []

        for location in LOCATIONS:
            endpoint = (
                f"/v1/forecast?"
                f"latitude={location['latitude']}&"
                f"longitude={location['longitude']}&"
                f"current_weather=true"
            )
            response = http_hook.run(endpoint)
            if response.status_code == 200:
                data = response.json()
                data["location"] = location
                weather_data_list.append(data)
            else:
                raise Exception ("failed to fetch data")
        
        return weather_data_list
    ### extracted data : weaher_data_list

    @task()
    def transform_weather_data(weather_data_list):

        transformed_data_list = []

        for data in weather_data_list:
            location = data['location']
            current_weather = data['current_weather']

            transformed_data= {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'temperature': current_weather['temperature'],
                'windspeed': current_weather['windspeed'],
                'winddirection': current_weather['winddirection'],
                'weathercode': current_weather['weathercode']
            }
            transformed_data_list.append(transformed_data)

        return transformed_data_list
    ### transformed data : transformed_data_list

    @task()
    def load_weather_data(transformed_data_list):

        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        for record in transformed_data_list:
            cursor.execute("""
                    INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
                    VALUES (%s, %s, %s, %s, %s, %s)  
                        """,(
                            record['latitude'],
                            record['longitude'],
                            record['temperature'],
                            record['windspeed'],
                            record['winddirection'],
                            record['weathercode']
                        ))
        conn.commit()
        conn.close()

    ### Workflow
    weather_data_list = extract_weather_data()     #Extraction

    transformed_data_list = transform_weather_data(weather_data_list)     #Transformation

    load_weather_data(transformed_data_list)     #Loading

