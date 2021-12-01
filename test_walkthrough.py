from pywebio.output import PopupSize, close_popup, popup, put_button, put_buttons, put_column, put_html, put_markdown, put_row, put_text, style, put_image, use_scope
from pywebio.pin import pin
from pywebio.session import go_app
from classes.test import Test
from cookie_io import get_current_test_id, get_current_user_id, init_js_cookie_io, remove_test_info, remove_user_info, set_free_mode
from sql import get_q_answers, get_test_by_id, get_test_questions, get_user_by_id, register_test_session_results, update_test_after_play
from utils import put_empty_row, centered_container, run_after_ok_popup
from styles import *
from pywebio.pin import put_radio

# глобальные переменные страницы
page_globals = {
    'current_user': None,
    'current_test': None,
    'question_set': None,
    'current_question': None,
    'current_q_index': 0,
    'current_answer_set': None,
    'current_score': 0
}


# логгирование модуля
def log(message: str):
    print(f'[Прохождение теста] {message}...')


# затереть данные 
def clear_page_globals():
    log('Очистка данных модуля')
    global page_globals
    page_globals = {
        'current_user': None,
        'current_test': None,
        'question_set': None,
        'current_question': None,
        'current_q_index': 0,
        'current_answer_set': None,
        'current_score': 0
    }


# получение списка вопросов
def init_questions():
    log('Получение вопросов')
    global page_globals
    page_globals['question_set'] = get_test_questions(page_globals['current_test'].id)
    page_globals['current_question'] = page_globals['question_set'][page_globals['current_q_index']]
    page_globals['current_score'] = 0
    

# получение теста
def init_test():
    log('Получение теста')
    global page_globals
    id = get_current_test_id()
    if(id != None):
        test = get_test_by_id(id)
        if(test != None):
            page_globals['current_test'] = test


# получение пользователя
def init_user():
    log('Получение пользователя')
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user
    else:
        clear_page_globals()
        go_app('auth_page', new_window=False)


# инициализация глобальных переменных страницы
def init_page_globals():
    log('Начало инициализации глобальных переменных страницы')
    global page_globals
    init_user()
    init_test()
    init_questions()

    
# переход на следующий вопрос
def increment():
    log('Обработка ответа')
    global page_globals
    answer_id = pin.answer_radio
    is_true = answer_id in [answer.id for answer in page_globals['current_answer_set'] if answer.is_right]
    
    page_globals['current_score'] += 1 if is_true else 0
    page_globals['current_q_index'] += 1
   
    if(page_globals['current_q_index'] > len(page_globals['question_set']) - 1):
        end_test()
    else:
        page_globals['current_question'] = page_globals['question_set'][page_globals['current_q_index']]
        log(f'Переход на следующий вопрос, счёт: {page_globals["current_score"]}')
        centered_container(test_question_scope())


# окончание теста - переход к странце с результатами
def end_test():
    global page_globals
    log(f'Закрытие теста, конечный счёт - {page_globals["current_score"]}/{page_globals["current_q_index"]}')
    # засетить результат с текущей датой
    register_test_session_results(
        page_globals['current_user'].id, 
        page_globals['current_test'].id,
        page_globals['current_score']
    )
    # обновить тест
    update_test_after_play(page_globals['current_test'].id)
    # затереть куки и глобальные переменные
    remove_test_info()
    set_free_mode()
    clear_page_globals()
    # отобразить страницу с результатом
    log('Переход на страницу с результатами')
    go_app('results_page', new_window=False)


# формирование списка ответов из радио-кнопкок
def answer_radio_button_group(question):
    global page_globals
    answers = get_q_answers(question.id)
    page_globals['current_answer_set'] = answers
    if(len(answers) > 0):
        current_selected_answer = put_radio('answer_radio', options=[
            { 'label': answer.answer_text, 'value': answer.id} for answer in answers
        ])
        return current_selected_answer
    else:
        return put_text('нет ответов')


# обновляемый контейнер текущего вопроса (при переходе на следующий вопрос контейнер перерисовывается)
@use_scope('test_question_scope', clear=True)
def test_question_scope():
    question = page_globals['question_set'][page_globals['current_q_index']]
    photo = question.question_photo_url
    photo = '\n' if photo == None else f'![Картинка вопроса]({photo})'
    
    md_text = ''
    md_text += f'### Вопрос №{page_globals["current_q_index"]+1}: {page_globals["current_question"].question}\n'

    button_label = 'Ответить' if page_globals['current_q_index'] < len(page_globals['question_set'])-1 else 'Закончить тест'

    if(question.question_photo_url == None):
        return put_column([
            put_markdown(md_text),
            answer_radio_button_group(question),
            put_button(label=button_label, onclick=increment)
        ])
    else:
        return put_column([
            put_markdown(md_text),
            put_image(question.question_photo_url, width='400px', height='400px'),
            answer_radio_button_group(question),
            put_button(label='Добавить', onclick=increment)
        ])


# переход на страницу листов
def quit_test():
    # стереть все и выйти
    log(f'Переход на страницу тестов - счёт: {page_globals["current_score"]}/{page_globals["current_q_index"]}')
    remove_test_info()
    set_free_mode()
    clear_page_globals()
    go_app('test_list_page', new_window=False)


# хедер страницы вопроса
def test_play_header():
    return put_row(
            [put_markdown(f'# Тест \"{page_globals["current_test"].name}\"'), 
                None,
                style(
                    put_row([
                        put_buttons(['Закончить тест', 'Выйти из теста'], [end_test, quit_test]),
                        put_text(f'Тест в процессе')
                    ]), 'align-self: center')
            ], size='60% 200px 40%'
        )


# основной код страницы
def test_play_page():
    log('Загрузка страницы')
    init_js_cookie_io()
    init_page_globals()

    if(page_globals['current_user'] == None):
        log('Пользователь не авторизован. Переход на страницу авторизации')
        clear_page_globals()
        set_free_mode()
        remove_user_info()
        go_app('auth_page', new_window=False)
    if page_globals['current_test'] == None:
        log('Тест не загружен, переход на страницу тестов')
        go_app('test_list_page', new_window=False)
    else:   
        test_play_header()
        put_empty_row()
        centered_container(test_question_scope())