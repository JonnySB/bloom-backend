from lib.models.help_request import HelpRequest
class HelpRequestRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def all_requests(self):
        rows = self.db_connection.execute("SELECT * FROM help_requests ORDER BY id")
        help_requests = []
        for row in rows:
            obj = HelpRequest(
                row["id"], 
                row["user_id"], 
                row["timestamp"], 
                row["title"], 
                row["message"], 
                row["plant"], 
                row["date_range"], 
                row["max_price"]
            )
            help_requests.append(obj)
        return help_requests
    

    def find_request_by_id(self, help_request_id):
        try:
            help_request_id = int(help_request_id)
        except ValueError:
            return None
        rows = self.db_connection.execute(
            "SELECT * FROM help_requests WHERE id = %s", 
            [help_request_id])
        row = rows[0]
        return HelpRequest(row["id"], row["user_id"], row["timestamp"], row["title"], row["message"], row["plant"], row["date_range"], row["max_price"])
    
    def find_request_by_plant():
        pass

    def create_request(self, help_request):
        self.db_connection.execute(
            "INSERT INTO help_requests (user_id, timestamp, title, message, plant, date_range) VALUES (%s, %s, %s, %s, %s, %s)",
            [help_request.user_id, help_request.timestamp, help_request.title, help_request.message, help_request.plant, help_request.date_range]
        )
        return None
    

    def update_help_request_by_id(self, help_request_id, new_values):
        existing_help_request = self.find_request_by_id(help_request_id)

        if existing_help_request is None:
            return "Help request id does not exist"
    
        if isinstance(new_values, str):
            new_values = {"", new_values}

        for field, value in new_values.items():
            setattr(existing_help_request, field, value)

        set_clause = ', '.join([f'{field} = %s' for field in new_values.keys()])

        query = f"UPDATE help_requests SET {set_clause} WHERE id = %s"

        self.db_connection.execute(query, list(new_values.values()) + [help_request_id])

        return None
    