from pyspark.sql.session import SparkSession


def get_spark_session():
    spark = (
        SparkSession.builder
        .appName("DataEngineerChallenge")
        .config("spark.mongodb.input.uri", "mongodb://root:rootpassword@mongo:27017/sensors_db.sensors_data")
        .config("spark.mongodb.output.uri", "mongodb://root:rootpassword@mongo:27017/sensors_db.sensors_data")
        .config("spark.sql.shuffle.partitions", 4)
        .config("spark.executor.memory", "2g")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )
    return spark