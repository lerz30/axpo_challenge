FROM python:3.10-alpine

RUN apk add --no-cache openjdk11 bash

# Setting environment variables for Java and Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Downloading and installing Spark 3.5.0
RUN wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz -O /opt/spark.tar.gz && \
    tar -xzf /opt/spark.tar.gz -C /opt && \
    mv /opt/spark-3.5.0-bin-hadoop3 /opt/spark && \
    rm /opt/spark.tar.gz

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY . .

