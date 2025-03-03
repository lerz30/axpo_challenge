import json
from datetime import datetime

import paho.mqtt.client as mqtt
from pymongo.mongo_client import MongoClient

from exceptions.exceptions import ConsumptionException, MongoException
from settings import get_settings


class Consumer:
    def __init__(self):
        self.settings = get_settings()
        self.broker_host = self.settings.mqtt.host
        self.broker_port =  self.settings.mqtt.port
        self.topic = self.settings.mqtt.topic

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.mongo_client = MongoClient(self.settings.mongo.uri)
        self.db_name = self.mongo_client[self.settings.mongo.db_name]
        self.collection_name = self.db_name[self.settings.mongo.collection_name]

    def on_connect(self, client, userdata, flags, rc):
        """
        This is a callback method that can be found in paho.mqtt.client. Return code (rc) with a value of zero
        means connection has been established successfully. Any other value indicates error
        """
        if rc == 0:
            print(f"Successfully connected at {self.broker_host}:{self.broker_port}")
            client.subscribe(self.topic)
            print(f"Successfully subscribed to topic: {self.topic}")

        print(f"Connection failed with the following response code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            message_data = json.loads(msg.payload.decode())
            document = {
                "id": message_data["id"],
                "dt": message_data["dt"],
                "value": message_data["value"],
                "topic": self.topic,
                "creation_timestamp": datetime.utcnow()
                }
        except ConsumptionException as e:
            print(f"{e} \nTopic: {self.topic}")
        else:
            self.insert_to_mongo(document=document)

    def _create_mongo_db_collection(self):
        # TODO: don't hardcode the collection_name sensors_data.
        db = self.mongo_client["sensors_db"]
        if "sensors_data" not in db.list_collection_names():
            db.create_collection("sensors_data")
            print(f"Collection created successfully...")

    def insert_to_mongo(self, document):
        try:
            self.collection_name.insert_one(document)
            print(f"Document inserted successfully successfully!")
        except MongoException as e:
            print(f"{e} - message_id: {document['id']} topic: {document['topic']}")

    def start(self):
        self._create_mongo_db_collection()
        self.client.connect(host=self.broker_host, port=self.broker_port)
        self.client.loop_forever()
