# encoding: utf-8

def log_message(message_as_text):
    print(message_as_text)
    message_as_text = message_as_text + "\n"
    f = open("log", "a+")
    f.write(message_as_text)
    f.close()