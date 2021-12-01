from pywebio.output import toast

message: str = None

def set_message(new_message):
    global message
    message = new_message

def show_message():
    global message
    if message is not None:
        toast(message, duration=2, color='info')
        message = None