from settings import get_settings
from spark.spark_session import get_spark_session
from pyspark.sql.functions import col, lower


class SparkProcess:
    def __init__(self):
        self.spark = get_spark_session()
        self.settings = get_settings()
        self.postgres_jdbc_url = f"jdbc:postgresql://postgres:{self.settings.postgres.port}/{self.settings.postgres.db_name}"
        self.postgres_properties = {
            "user": self.settings.postgres.username,
            "password": self.settings.postgres.password,
            "driver": "org.postgresql.Driver"
        }

    def process(self):
        input_df = self.read_input_data()
        normalized_data_df = self.normalize_data(input_df)
        self.write_to_postgres(normalized_data_df)

    def read_input_data(self):
        print("Reading data from MongoDB")
        mongo_setting = self.settings.mongo
        input_df = (
            self.spark.read
            .format("mongo")
            .option("uri", f"{mongo_setting.uri}")
            .load()
        )
        return input_df

    @staticmethod
    def normalize_data(input_df):
        """
        Lowers the id column for normalization
        """
        print("Normalizing data")
        normalized_data_df = (
            input_df
            .withColumn("id", lower(col("id")))
            .drop("_id")
        )
        return normalized_data_df

    def write_to_postgres(self, normalized_data):
        """
        Persists data to POstgres
        """
        print("Writing data to Postgres")
        normalized_data.write.jdbc(
            url=self.postgres_jdbc_url,
            table="sensors",
            mode="append",
            properties=self.postgres_properties
        )
