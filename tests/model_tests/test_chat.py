from lib.models.chat import Chat


def test_chat():
    chat = Chat(1, 2,"Hello user 02","2023-10-19 10:23:54", "2023-10-19 10:23:54",  1)
    assert chat.id == 1
    assert chat.recipient_id == 2
    assert chat.message == "Hello user 02"
    assert chat.start_date == "2023-10-19 10:23:54"
    assert chat.end_date == "2023-10-19 10:23:54"
    assert chat.sender_id == 1


def test_chat_format():
    chat = Chat(1, 2, "Hello user 02","2023-10-19 10:23:54","2023-10-19 10:23:54", 1)
    assert str(chat) == "Chat(1, 2, Hello user 02, 2023-10-19 10:23:54, 2023-10-19 10:23:54, 1)"

