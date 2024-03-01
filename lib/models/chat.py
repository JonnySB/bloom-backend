class Chat:
    def __init__(self, id, recipient_id, message, start_date, end_date, sender_id):
        self.id = id
        self.recipient_id = recipient_id
        self.message = message
        self.start_date = start_date,
        self.end_date = end_date,
        self.sender_id = sender_id
    
    # Below I am compar9jgn chat with itself if not then I compare with another object type. 
    # ensuring that that two Chat objects are considered equal if and only if all their corresponding attributes are equal. 
    # This is useful when we need to compare Chat objects, 
    # for example, to check if a specific chat message already exists in a collection, or to ensure that tests are accurately comparing expected and actual Chat objects.
    def __eq__(self, other):
            if not isinstance(other, Chat):
                return False
            return (self.id == other.id and
                    self.recipient_id == other.recipient_id and
                    self.message == other.message and
                    self.start_date == other.start_date and
                    self.end_date == other.end_date and
                    self.sender_id == other.sender_id)
    
    def __repr__(self):
        return f"Chat({self.id}, {self.recipient_id}, {self.message}, {self.start_date}, {self.end_date}, {self.sender_id})"