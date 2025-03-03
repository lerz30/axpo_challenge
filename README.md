# Data Engineer - Challenge

The general approach to solve the challenge was to create a process with the ability to connect to the broker, 
subscribe to the topic and consume all messages being pushed by the generator, to then write them into a collection in 
MongoDB. To implement it, the MQQT client was used. It first connects to MongoDB, checks if the data collection already 
exists, if not, it creates it and finally connects to the broker and subscribes to the topic and start reading messages.
Each read message is persisted as a document in MongoDB. Previously a MongoDB service is defined in the 
docker-compose.yaml.

For the second part, the idea was to create a Spark SQL process with the ability to read the data from MongoDB, 
apply some transformation and persist the data in Postgres, which would act as a data warehouse. To do this, a postgres 
service was defined in the docker-compose.yaml, as well as a two Spark container: one master and one client.
The Dockerfile was modified to install Java, Spark and set the corresponding environment variables. For this part, 
an issue with mongo-spark-connector_2.12:10.4.1 didn't allow the Spark process to connect to MongoDb and
read the data.