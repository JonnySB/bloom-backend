from lib.models.help_request import HelpRequest


class HelpRequestRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def all_requests(self):
        rows = self.db_connection.execute("SELECT * FROM help_requests ORDER BY id;")
        help_requests = []
        for row in rows:
            obj = HelpRequest(
                row["id"],
                row["date"],
                row["title"],
                row["message"],
                row["start_date"],
                row["end_date"],
                row["user_id"],
                row["maxprice"],
            )
            help_requests.append(obj)
        return help_requests

    # To find one existing request by id
    def find_request_by_id(self, request_id):
        try:
            request_id = int(request_id)
        except ValueError:
            return None

        rows = self.db_connection.execute("""
            SELECT distinct on (hr.id)
				hr.*, 
                u.first_name, 
                u.last_name, 
                u.username, 
                u.avatar_url_string,
                p.photo AS plant_photo
            FROM help_requests hr
            JOIN users u ON hr.user_id = u.id
            JOIN user_plants up ON hr.user_id = up.user_id
            JOIN plants p ON up.plant_id = p.id
            WHERE hr.id = %s;
        """, [request_id])
        
        if not rows:
            return None
        
        row = rows[0]
        help_request = HelpRequest(
            row["id"], 
            row["date"], 
            row["title"], 
            row["message"], 
            row["start_date"], 
            row["end_date"],
            row["user_id"], 
            row["maxprice"]
        )
        user_details = {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "username": row["username"],
            "avatar_url_string": row["avatar_url_string"]
        }
        plant_photo = row["plant_photo"]
        
        return help_request, user_details, plant_photo




    # As an endpoint that when a user enters a substring of a title, they can find all the requests that have this substring
    # For example, if a user enters the word "water", then all the requests that has this substring will be returned
    def find_requests_by_title_substring(self, title):
        query = "SELECT * FROM help_requests WHERE title LIKE %s"
        title_lookup = f"%{title}%"
        rows = self.db_connection.execute(query, [title_lookup])

        help_requests = []
        for row in rows:
            obj = HelpRequest(
                row["id"],
                row["date"],
                row["title"],
                row["message"],
                row["start_date"],
                row["end_date"],
                row["user_id"],
                row["maxprice"],
            )
            help_requests.append(obj)

        return help_requests

        # "id": offer.id,
        # "user_id": offer.user_id,
        # "request_id": offer.request_id,
        # "message": offer.message,
        # "bid": offer.bid,
        # "status": offer.status

    # to find all requests made to a specific user
    def find_requests_by_user_id(self, user_id):
        query = "SELECT * FROM help_requests WHERE user_id = %s"
        rows = self.db_connection.execute(query, [user_id])

        help_requests_by_user = []
        for row in rows:
            obj = HelpRequest(
                row["id"],
                row["date"],
                row["title"],
                row["message"],
                row["start_date"],
                row["end_date"],
                row["user_id"],
                row["maxprice"],
            )
            help_requests_by_user.append(obj)

        return help_requests_by_user

    def create_request(self, help_request):
        self.db_connection.execute(
            "INSERT INTO help_requests (date, title, message, start_date, end_date, user_id, maxprice) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            [
                help_request.date,
                help_request.title,
                help_request.message,
                help_request.start_date,
                help_request.end_date,
                help_request.user_id,
                help_request.maxprice,
            ],
        )
        return None

    # To update an exisiting help request by any field whether it be title, date, message, start_date or end_date
    def update_help_request_by_id(self, request_id, new_values):
        existing_request = self.find_request_by_id(request_id)

        if existing_request is None:
            return None

        for field, value in new_values.items():
            setattr(existing_request, field, value)

        set_clause = ", ".join([f"{field} = %s" for field in new_values.keys()])

        query = f"UPDATE help_requests SET {set_clause} WHERE id = %s"
        values = list(new_values.values()) + [request_id]
        self.db_connection.execute(query, values)

        return None

    # To delete an existing request from the database
    def delete_request(self, user_id, request_id):
        existing_request = self.find_request_by_id(request_id)

        if existing_request is None:
            return None

        self.db_connection.execute(
            "DELETE FROM help_requests WHERE user_id =%s AND id = %s", [user_id, request_id]
        )
        return None
    
    def get_all_help_requests_with_user_first_name_and_last_name(self):
        rows = self.db_connection.execute("SELECT help_requests.*, users.first_name, users.last_name, users.username, users.avatar_url_string FROM help_requests JOIN users ON help_requests.user_id = users.id;")

        help_requests_with_user_details = []
        for row in rows:
            help_request = HelpRequest(
                row["id"],
                row["date"],
                row["title"],
                row["message"],
                row["start_date"],
                row["end_date"],
                row["user_id"],
                row["maxprice"]
            )
            user_details = {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "avatar_url_string": row["avatar_url_string"]
            }
            help_requests_with_user_details.append((help_request, user_details))
        return help_requests_with_user_details
    
    def get_plant_photo_with_user_details_for_help_request(self):
        rows = self.db_connection.execute("""
                SELECT distinct on (hr.id)
                    hr.*,
                    u.first_name,
                    u.last_name,
                    u.avatar_url_string,
                    p.photo AS plant_photo
                FROM 
                    help_requests hr
                JOIN 
                    user_plants up ON hr.user_id = up.user_id
                JOIN 
                    plants p ON up.plant_id = p.id
                JOIN
                    users u ON hr.user_id = u.id;
                """)
        # rows = self.db_connection.execute(query)

        help_requests_with_details = []
     
        for row in rows:
            help_request = HelpRequest(
                row["id"],
                row["date"],
                row["title"],
                row["message"],
                row["start_date"],
                row["end_date"],
                row["user_id"],
                row["maxprice"]
            )
            user_details = {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "avatar_url_string": row["avatar_url_string"]
            }
            plant_photo = row["plant_photo"]
            help_requests_with_details.append((help_request, user_details, plant_photo))
        return help_requests_with_details
