from docker.types import Mount
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from Aggregations import pred_agr

# General parameters for the file
raw_path = "/opt/airflow/data/raw/data__{{ ds }}.csv"  # initialized data (from to)
predictin_path = "/opt/airflow/data/predict/labels__{{ ds }}.json"  # path to prediction path
result_path = "/opt/airflow/data/results/result__{{ ds }}.json"
model_name = 'Crypto_news'
experiment_name = 'valhalla_prediction'
run_name = 'classification_news_site'

# We mount files for Docker
mount_data_to_docker_airflow = {
    "mount_tmp_dir": False,  # do not save temporary files
    "mounts": [
        Mount(
            source="absolute path to data", # The absolute path to data in the project
            # path to file system (from AirFlowProject to data)
            target="/opt/airflow/data/",  # path to airflow container
            type="bind"  # mount from host to container

        )
    ],
    "retries": 1,  # repeats
    "api_version": "1.44",
    # "docker_url": "tcp://docker-socket-proxy:2375",
    "network_mode": "bridge",
}


# Create DAG. name, time, start, complete tasks before the specified date
@dag(dag_id='dag_for_news', schedule_interval="@daily", start_date=days_ago(0), catchup=False)
def function_for_each_tack_flow() -> None:
    """
    A function describing the DAG airflow

    load_data: task for getting data
    model_prediction_data: task for processing data and getting prediciton
    result_topic: task for preparing and writing the result to a file

    :return: -> None
    """
    # Task 1. load_data.py
    load_data = DockerOperator(
        task_id="load_data",
        image="load_data2:latest",
        command=f"python load_data.py --data_path {raw_path}",
        **mount_data_to_docker_airflow,
    )

    # Task 2. model_predict.py
    model_prediction_data = DockerOperator(
        task_id='model_prediction_data',
        image='model_prediction_data2:latest',
        command=f"python model_prediction.py --data_path {raw_path} --predictin_path {predictin_path} --experiment_name {experiment_name} --run_name {run_name} --model_name {model_name}",
        **mount_data_to_docker_airflow,
    )

    # Task 3. Result
    result_topic = PythonOperator(
        task_id='result_topic',
        python_callable=pred_agr,
        op_kwargs={
            'predictin_path': predictin_path,
            'result_path': result_path,
        },

    )
    load_data >> model_prediction_data >> result_topic


function_for_each_tack_flow()
