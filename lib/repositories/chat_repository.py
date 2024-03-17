from lib.models.chat import Chat
from datetime import datetime, timedelta

class ChatRepository:
    def __init__(self, connection):
        self._connection = connection
    

    def find_messages_by_userid(self, user_id):
        query = '''
            SELECT 
                c.*, 
                ru.username AS receiver_username, 
                su.username AS sender_username 
            FROM 
                chats c
                JOIN users ru ON c.recipient_id = ru.id 
                JOIN users su ON c.sender_id = su.id 
            WHERE 
                c.sender_id = %s OR c.recipient_id = %s
        '''
        rows = self._connection.execute(query, [user_id, user_id])
        
        grouped_messages = {}
        for row in rows:
            key = frozenset([row['sender_id'], row['recipient_id']])
            if key not in grouped_messages:
                grouped_messages[key] = []
            grouped_messages[key].append(row)

        most_recent_messages = []
        for messages in grouped_messages.values():
            most_recent_message = max(messages, key=lambda msg: msg['end_date'])  
            most_recent_messages.append(most_recent_message)

        messages_cleaned = []
        for msg in most_recent_messages:
            message_text = msg['message']
            message = {
                'message': Chat(msg['id'], msg['recipient_id'], message_text, msg['start_date'], msg['end_date'], msg['sender_id']),
                'receiver_username': msg['receiver_username'],
                'sender_username': msg['sender_username']
            }
            messages_cleaned.append(message)

        return messages_cleaned
    
    
    
    def find_message_by_chat_id(self, chat_id):
           message = self._connection.execute('SELECT * from chats WHERE id=%s', [chat_id])
           return message


    def create(self, sender, receiver, message, receiver_username, sender_username):
        today_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        start_date = datetime.now() - timedelta(days=30)
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        end_date = datetime.now() + timedelta(days=30)
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        query = '''SELECT * FROM chats WHERE ((recipient_id = %s AND sender_id = %s) OR (recipient_id = %s AND sender_id = %s)) AND %s BETWEEN start_date AND end_date'''
        existing_chat = self._connection.execute(query, [receiver, sender, sender, receiver, today_str])
       
        message_with_username = f'{{"sender": "{sender_username}", "message": "{message}"}}'
      
        if existing_chat:
            # Existing chat found, so append message to it
            update_query = '''UPDATE chats SET message = array_append(message, %s), end_date = %s WHERE id = %s RETURNING *;'''
            result = self._connection.execute(update_query, [message_with_username, end_date_str, existing_chat[0]['id']])
        else:
            # No existing chat found, so insert a new chat record
            insert_query = '''INSERT INTO chats (recipient_id, message, start_date, end_date, sender_id, receiver_username, sender_username) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;'''
            result = self._connection.execute(insert_query, [receiver, [message_with_username], start_date_str, end_date_str, sender, receiver_username, sender_username])

     
        for row in result:
            row['start_date'] = row['start_date'].isoformat()
            row['end_date'] = row['end_date'].isoformat()

        return result




    

#  FOR NOW JUST adding the create and find, in the future we will be  implementing update and delete 
