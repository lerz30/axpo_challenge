class ConsumptionException(Exception):
    def __init__(self, message="There's been an issue while consuming the messages"):
        super().__init__(message)

class MongoException(Exception):
    def __init__(self, message="There's been an error inserting the document into MongoDB"):
        super().__init__(message)