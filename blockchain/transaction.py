import time
import uuid

class Transaction:
    def __init__(
        self,
        sender,
        recipient,
        product_id,
        product_name,
        location=None,
        temperature=None,
        humidity=None,
        transport_info=None,
        status=None,
        timestamp=None,
        id=None,
        expiry_date=None
    ):
        
        self.id = id if id else str(uuid.uuid4())
        
        self.sender = sender
        self.recipient = recipient
        self.product_id = product_id
        self.product_name = product_name
        self.location = location
        self.temperature = temperature
        self.humidity = humidity
        self.transport_info = transport_info
        self.status = status
        self.timestamp = timestamp or time.time()
        self.expiry_date = expiry_date

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'location': self.location,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'transport_info': self.transport_info,
            'status': self.status,
            'timestamp': self.timestamp,
            'expiry_date': self.expiry_date
        }

    def __repr__(self):
        return f"Transaction<{self.product_name}, {self.sender} -> {self.recipient}>"
