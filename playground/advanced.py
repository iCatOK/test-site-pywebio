from pywebio.platform import start_server
from pywebio.output import put_link, put_text, put_buttons
from pywebio.session import go_app


def task_1():
    put_text('task_1')
    put_buttons(['Go task 2', 'Print console'], [lambda: go_app('task_2', new_window=False), lambda: print('aaaaa')])

def task_2():
    put_text('task_2')
    put_buttons(['Go task 1'], [lambda: go_app('task_1', new_window=False)])

def index():
    put_link('Go task 1', app='task_1')  # Use `app` parameter to specify the task name
    put_link('Go task 2', app='task_2')

# equal to `start_server({'index': index, 'task_1': task_1, 'task_2': task_2})`
start_server([index, task_1, task_2], port=8080)