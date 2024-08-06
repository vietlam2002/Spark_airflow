import airflow
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

import os
airflow_home = os.environ['AIRFLOW_HOME']
dag = DAG(
    dag_id = "sparking_flow",
    default_args = {
        "owner": "Yusuf Ganiyu",
        "start_date": airflow.utils.dates.days_ago(1)
    },
    start_date=datetime(2024, 8, 3),
    end_date=datetime(2024, 8, 6),
    schedule_interval = "@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

# python_job = SparkSubmitOperator(
#     task_id="python_job",
#     conn_id="spark-conn",
#     application="jobs/python/wordcountjob.py",
#     dag=dag
# )
#
# scala_job = SparkSubmitOperator(
#     task_id="scala_job",
#     conn_id="spark-conn",
#     application="jobs/scala/target/scala-2.12/word-count_2.12-0.1.jar",
#     dag=dag
# )
#
# java_job = SparkSubmitOperator(
#     task_id="java_job",
#     conn_id="spark-conn",
#     application="jobs/java/spark-job/target/spark-job-1.0-SNAPSHOT.jar",
#     java_class="com.airscholar.spark.WordCountJob",
#     dag=dag
# )
python_job = BashOperator(
    task_id="python_job",
    bash_command=f'python {airflow_home}/jobs/python/wordcountjob.py'
)
scala_job = EmptyOperator(
    task_id="scala_job"
)

java_job = EmptyOperator(
    task_id="java_job",
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> [python_job, scala_job, java_job] >> end
