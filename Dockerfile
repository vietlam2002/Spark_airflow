FROM apache/airflow:2.7.1-python3.10

USER root
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    scala \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"


# Install Spark (optional: you can choose the version you need)
RUN curl -sL "https://downloads.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz" | tar xz -C /opt \
    && mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark
