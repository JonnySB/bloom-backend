from lib.models.chat import Chat
from datetime import datetime, timedelta


class ChatRepository:
    def __init__(self, connection):
        self._connection = connection
     
    
    def find_messages_by_userid(self, user_id):
        rows = self._connection.execute('SELECT up.*, p.username AS receiver_username FROM chats up JOIN users p ON up.recipient_id = p.id WHERE up.sender_id = %s', [user_id])
        messages = []
        for row in rows:
            message_text = row['message']
            message = { 'message': Chat(row['id'], row['recipient_id'], message_text, row['start_date'], row['end_date'], row['sender_id']),
                        'receiver_username': row['receiver_username']
                       }
            messages.append(message)
        return messages
        
    
        # the logic is we will only show messages that are 30 days old to avoid creating multiple messages in the database. if there is a chat between the users within the last 30 days, then we will append the new message to an array,
        #otherwise we will create a new message
    
    def find_message_by_chat_id(self, chat_id):
           message = self._connection.execute('SELECT * from chats WHERE id=%s', [chat_id])
           return message


    def create(self, sender, receiver, message, receiver_username):
        today_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        start_date = datetime.now() - timedelta(days=30)
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        end_date = datetime.now() + timedelta(days=30)
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        query = '''SELECT * FROM chats WHERE ((recipient_id = %s AND sender_id = %s) OR (recipient_id = %s AND sender_id = %s)) AND %s BETWEEN start_date AND end_date'''
        existing_chat = self._connection.execute(query, [receiver, sender, sender, receiver, today_str])
        print(sender)
        if existing_chat:
            # Existing chat found, so append message to it
            update_query = '''UPDATE chats SET message = array_append(message, %s) WHERE id = %s RETURNING *;'''
            result = self._connection.execute(update_query, [message, existing_chat[0]['id']])
        else:
            # No existing chat found, so insert a new chat record
            insert_query = '''INSERT INTO chats (recipient_id, message, start_date, end_date, sender_id, receiver_username) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;'''
            result = self._connection.execute(insert_query, [receiver, [message], start_date_str, end_date_str, sender, receiver_username])

     
        for row in result:
            row['start_date'] = row['start_date'].isoformat()
            row['end_date'] = row['end_date'].isoformat()

        return result




    

#  FOR NOW JUST adding the create and find, in the future we will be  implementing update and delete 