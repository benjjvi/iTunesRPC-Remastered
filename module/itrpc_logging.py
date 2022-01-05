# encoding: utf-8

def log_message(message_as_text):
    print(message_as_text)
    message_as_text = message_as_text + "\n"
    with open("log", "a+", encoding="utf-8") as f:
        f.write(message_as_text)