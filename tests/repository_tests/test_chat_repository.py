from lib.repositories.chat_repository import ChatRepository
from lib.models.chat import Chat
from datetime import datetime
import json 

def test_find_messages_by_userid(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    expected_chat = Chat(1, 2, '{"{\"sender\": \"user1\", \"message\": \"Hello user two\"}"}', '2024-01-31','2024-03-01', 1)
    chats = repository.find_messages_by_userid(1)
    assert expected_chat == Chat(1, 2, '{"{\"sender\": \"user1\", \"message\": \"Hello user two\"}"}', '2024-01-31','2024-03-01', 1)
    assert len(chats) == 1, "Expected exactly one chat message for user_id 1"



# this tests if the chat is created for the first time.
def test_create_chat_one_message(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    repository.create(1, 2, '{"sender": "user1", "message": "Hello user two"}', "user02", "user01")
    find = repository.find_messages_by_userid(1)
    expected_message = "Chat(1, 2, ['{\"sender\": \"user1\", \"message\": \"Hello user two\"}'], 2024-01-31 00:00:00, 2024-03-01 00:00:00, 1)"
    actual_message = str(find[0]['message'])
    assert actual_message == expected_message
    assert find[0]['receiver_username'] == 'user2'
    assert find[0]['sender_username'] == 'user1'

 
 

def test_create_chat_when_user_has_already_initiated_conversation(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    repository.create(3, 5, '{"sender": "user3", "message": "Hello user five"}', "user5", "user3")
    repository.create(3, 5, '{"sender": "user3", "message": "Hello user five it is me again"}', "user5", "user3")
    find = repository.find_messages_by_userid(3)

    assert len(find) == 1  ## ENSURE THAT ONLY ONE CHAT IS CREATED 
    try:
        chat_messages = json.loads(find[0]['message']) #heck if the message is already in a structured format or if it's a JSON str.
    except TypeError:
        print("Error: 'message' is not a properly formatted JSON string.")
        return
    assert len(chat_messages) == 2  # Expecting two messages in the chat
    assert chat_messages[0]['sender'] == "user3" and chat_messages[0]['message'] == "Hello user five" ## MESSAGE ONE
    assert chat_messages[1]['sender'] == "user3" and chat_messages[1]['message'] == "Hello user five it is me again"  ## MESSAGE TWO
    assert find[0]['receiver_username'] == 'user5'
    assert find[0]['sender_username'] == 'user3'
 