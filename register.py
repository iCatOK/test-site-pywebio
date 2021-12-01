from logging import error
from pywebio.output import put_buttons, put_column, put_error, put_markdown, put_text, toast
from pywebio.input import NUMBER, PASSWORD, input_group
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from classes.user import User
from cookie_io import get_current_user_id, init_js_cookie_io, is_test_mode

from sql import register_user


# редирект в случае пойманных куки
def redirect():
    id = get_current_user_id()
    
    if id != None:
        go_app('test_list_page', new_window=False)
    
    if(is_test_mode()):
        go_app('test_play_page', new_window=False)


# обёртка - при ошибке регистрации возвращает сообщение об ошибке
def register():
    answer = register_user(pin.name, pin.username, pin.password)

    if(type(answer) is str):
        toast(answer, duration=3, color='error')

# переход на страницу авторизации
def to_login():
    go_app('auth_page', new_window=False)


# основной код страницы регистрации
def register_page():
    put_markdown('# 🆕 Регистрация')
    init_js_cookie_io()
    redirect()
    put_column([
        put_input('name', label='Имя'),
        put_input('username', label='Логин'),
        put_input('password', label='Пароль', type=PASSWORD)
    ])
    put_buttons(['Зарегистрироваться', 'Назад'], onclick=[register, to_login])