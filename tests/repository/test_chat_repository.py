from lib.repository.chat_repository import ChatRepository
from lib.models.chat import Chat
from datetime import datetime

def test_find_messages_by_userid(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    chats = repository.find_messages_by_userid(2)
    expected_chat = Chat(1, 2, 'Hello user 02', '2023-10-19 00:00:00', 1)
    assert len(chats) == 1, "Expected exactly one chat message for user_id 1"
    assert expected_chat == Chat(1, 2, 'Hello user 02', '2023-10-19 00:00:00', 1)



#this tests if the chat is created for the first time.
def test_create_chat_one_message(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    chat_01 = Chat(1, 2, ['Hello user 02'], datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 1)
    chat_02 = Chat(1, 1, ['Hello user 01'], datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 2)
    repository.create(chat_01, chat_02)
    find = repository.find_messages_by_userid(2)
    assert find[0].id == chat_01.id
    assert find[0].recipient_id == chat_01.recipient_id
    assert find[0].message == chat_01.message
    assert find[0].sender_id == chat_01.sender_id
    
   

#if chat has already been created then append the message into the existing message
def test_create_chat_when_user_has_already_iniate_conversation(db_connection):
    db_connection.seed('seeds/bloom.sql')
    repository = ChatRepository(db_connection)
    chat_01 = Chat(1, 2, 'Hello user 02', datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 1)
    chat_02 = Chat(1, 1, 'Hello user 01', datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 2)
    chat_03 = Chat(1, 2, 'Hello again user 02', datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 1)
    chat_04 = Chat(1, 1, 'Hello again user 01', datetime.strptime('2023-10-19 00:00:00', '%Y-%m-%d %H:%M:%S'), 2)
    repository.create(chat_01, chat_02)
    repository.create(chat_03, chat_04)
    find = repository.find_messages_by_userid(1)
    assert len(find) == 1 
    found_chat = find[0]
    expected_message = ['Hello user 01','Hello again user 01']
    assert found_chat.message == expected_message
    assert found_chat.recipient_id == 1
    
        
 