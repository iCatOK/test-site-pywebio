from pywebio.input import PASSWORD
from pywebio.output import put_button, put_buttons, put_column, put_markdown, put_row, put_text, span, style, put_image
from pywebio.pin import put_input
from pywebio.session import go_app
from classes.test import Test
import classes.user as user_info
import classes.test as test_info
from cookie_io import get_cookie, get_current_user_id, init_js_cookie_io, is_test_mode, remove_cookie, remove_user_info, save_current_test_id, set_test_mode
from sql import get_test_questions, get_tests, get_user_by_id
from utils import multi_markdown_text, put_empty_row, centered_container, test_cell_container
from styles import *


# глобальные переменные страницы
page_globals = {
    'current_user': None
}


# стереть глобальные переменные страницы
def clear_page_globals():
    global page_globals
    page_globals = {
        'current_user': None
    }


# получение пользователя из id в куки
def set_user_from_cookie():
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user


# выход из учетной записи
def logout():
    remove_user_info()
    clear_page_globals()
    go_app('auth_page', new_window=False)


# результаты
def results():
    go_app('results_page', new_window=False)


# код для описания теста
def test_cell_markdown(test: Test):
    markdown = ''
    markdown += f'### {test.name}\n'
    markdown += f'![Image of Yaktocat]({test.photo_url})'
    markdown += f'{test.description}'
    
    markdown += '\n'
    markdown += f'* Кол-во вопросов: {test.question_count}\n'
    markdown += f'* Прохождений: {test.play_count}\n'
    markdown += f'* Средний балл: {round(test.avg_score, 2) if test.avg_score != -1 else "-"}\n'

    return put_markdown(markdown)


# выбор конкретного теста
def go_to_test(test: Test):
    q_set = (get_test_questions(test.id) or [])
    print(f'Переход к тесту. Кол-во вопросов: {len(q_set)}')
    if(len(q_set) <= 0):
        go_app('test_list_page', new_window=False)
    else:
        save_current_test_id(test.id)
        set_test_mode()
        go_app('test_play_page', new_window=False)


# добавление одного теста
def put_test_cell(test: Test):
    return test_cell_container(
        put_column([
            test_cell_markdown(test),
            put_empty_row(),
            put_button('Пройти', onclick=lambda: go_to_test(test), color='success')
        ])
    )


# формирование контейнера со списком тестов
def put_test_list():
    test_cell_list = []
    test_set = get_tests()

    if(len(test_set) == 0):
        return put_text('Еще не загрузили ни одного теста. Ждите обновлений!')

    for test in test_set:
        test_cell_list.append(put_test_cell(test))
    return put_column(test_cell_list)


# основной код страницы выбора теста
def test_list_page():
    init_js_cookie_io()
    set_user_from_cookie()

    print(page_globals)

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)
    
    if(is_test_mode()):
        go_app('test_play_page', new_window=False)

    print()

    put_row(
        [put_markdown('# Выберете тест для прохождения'), 
            None, style(put_buttons(['Посмотреть свои результаты', 'Выйти'], [results, logout]), 'align-self: center')
        ], size='60% 10px 40%'
    )
    put_empty_row()
   
    centered_container(put_test_list())
    

    
