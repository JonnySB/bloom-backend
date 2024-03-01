from lib.models.chat import Chat
import datetime
import json

class ChatRepository:
    def __init__(self, connection):
        self._connection = connection
    
    
    def find_messages_by_userid(self, user_id):
        rows = self._connection.execute('SELECT * from chats WHERE sender_id=%s', [user_id])
        messages = []
        for row in rows:
            message_text = row['message']
            message = Chat(row['id'], row['recipient_id'], message_text, row['date'], row['sender_id'])
            messages.append(message)
        return messages
        
    
        # the logic is we will only show messages that are 30 days old to avoid creating multiple messages in the database. if there is a chat between the users within the last 30 days, then we will append the new message to an array,
        #otherwise we will create a new message

    def create(self,receiver, sender):
        start_date = datetime.datetime.now() - datetime.timedelta(days=30)  # Calculate date 30 days ago from now
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days=30)  # Calculate date 30 days ago from now
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        
        # Check for existing chat between the recipient and sender in the last 30 days
        query = '''SELECT * FROM chats WHERE recipient_id = %s AND sender_id = %s AND date >= %s'''
        existing_chat = self._connection.execute(query, [receiver.id, sender.id, start_date_str])
        
        if not existing_chat:
            # If no messages in the last 30 days, insert the new message
            insert_query = '''INSERT INTO chats (recipient_id, message, date, sender_id) VALUES (%s, ARRAY[%s], %s, %s) RETURNING *;'''
            return self._connection.execute(insert_query, [receiver.id, receiver.message, datetime.datetime.now(), sender.id])
        else:
            # If there is an existing chat, append the new message to the existing 'message' field.
            # it is splited down by a comma so we can uset the split method in the future 
            update_query = '''UPDATE chats SET message = array_append(message, %s) WHERE recipient_id = %s AND sender_id = %s AND date >= %s RETURNING *;'''
            return self._connection.execute(update_query, [receiver.message, receiver.id, sender.id, start_date_str])


       




#  FOR NOW JUST adding the create and find, in the future we will be  implementing update and delete 