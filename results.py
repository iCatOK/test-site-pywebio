from pywebio.output import put_buttons, put_column, put_error, put_markdown, put_row, put_table, put_text, span, style
from pywebio.input import NUMBER, PASSWORD, input_group
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from classes.user import User
import classes.user as user_info
from messages import show_message
from cookie_io import get_current_user_id, init_js_cookie_io, is_test_mode, set_cookie
from sql import get_test_by_id, get_test_results_by_user, get_user_by_id, validate_credentials
from utils import centered_container, put_empty_row

user = None

# логгирование модуля
def log(message: str):
    print(f'[Результаты тестов] {message}...')


# редирект в случае пойманных куки
def redirect():
    log('Получение пользователя')
    global user
    user_id = get_current_user_id()
    
    if user_id == None:
        log('Пользователь не получен. Переход на страницу авторизации')
        go_app('auth_page', new_window=False) 
    
    if(is_test_mode()):
        log('Тест не закончен. Переход на страницу тестов')
        go_app('test_play_page', new_window=False)
    
    user = get_user_by_id(user_id)


# назад на страницу тестов
def back():
    go_app('test_list_page', new_window=False)


# таблица результатов
def result_table():
    return put_table()


# получение массива массивов для заполнения таблицы результатов
def get_results_tabled_data():
    results = get_test_results_by_user(user.id)
    table_data = [['Дата', 'Название теста', 'Счёт']]
    for result in results:
        test = get_test_by_id(result.test_id)
        date = result.date.strftime('%m/%d/%Y %H:%M:%S')
        table_data.append([date, test.name, result.score])
    return table_data


# основной код страницы результатов
def results_page():
    log('Загрузка страницы')
    init_js_cookie_io()
    redirect()
    put_row([
        put_markdown(f'# 🏆 Результаты пользователя {user.username}'),None,
        style(put_buttons(['Назад'], onclick=[back]), 'align-self: center')
    ], size='80% 300px 20%')
    put_empty_row()
    put_table(get_results_tabled_data())