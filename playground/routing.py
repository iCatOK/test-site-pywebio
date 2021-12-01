from pywebio.input import NUMBER, actions, file_upload, input, input_group
from pywebio.output import close_popup, output, popup, put_button, put_code, put_collapse, put_column, put_html, put_image, put_markdown, put_row, put_table, put_text, use_scope
from pywebio.platform.tornado import start_server
from pywebio.pin import put_input, put_select
import json

# info = input_group('Add user', [
#     input('username', type=TEXT, name='username', required=True),
#     input('password', type=PASSWORD, name='password', required=True),
#     actions('actions', [
#         {'label': 'Save', 'value': 'save'},
#         {'label': 'Save and add next', 'value': 'save_and_continue'},
#         {'label': 'Reset', 'type': 'reset'},
#         {'label': 'Cancel', 'type': 'cancel'},
#     ], name='action', help_text='actions'),
# ])
# put_code('info = ' + json.dumps(info, indent=4))
# if info is not None:
#     save_user(info['username'], info['password'])  
#     if info['action'] == 'save_and_continue':
#         add_next()  


def page_one():
    
    put_markdown('saasd')

    popup('Popup title', [
        put_html('<h3>Popup Content</h3>'),
        'plain html: <br/>',  # Equivalent to: put_text('plain html: <br/>')
        put_table([['A', 'B'], ['C', 'D']]),
        put_button('close_popup()', onclick=close_popup)
    ])
    
    start = input_group('Делание всякого', [
        input('Введите имя', placeholder='Имечко', required=True, name='name'),
        actions('Навигация', name='navigator', help_text='Выберете, куда отправиться', buttons=[
            {'label': 'Вперед', 'value': 'page_two'}
        ])
    ])

    router = get_router()
    
    if(start['navigator'] in router):
        router[start['navigator']]()

def page_two():
    pass

def page_three():
    put_markdown('Третья страница')

def get_router():
    return {
    'page_one': page_one,
    'page_two': page_two,
    'page_three': page_three
}

if __name__ == '__main__':
    start_server(page_one, debug=True, port=8081, cdn=False)


    