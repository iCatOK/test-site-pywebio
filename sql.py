import sqlite3
from datetime import datetime
from typing import Any, List

from pywebio.session import go_app
from pywebio.output import toast
from classes import user, test
from classes.test_answer import TestAnswer
from classes.test_question import TestQuestion
from classes.test_result import TestResult
from classes.user import User
from classes.test import Test
from sqlite3 import Error

from messages import set_message

db = sqlite3.connect('db.db', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)

# клиент бд
sql = db.cursor()


# запросы к бд
get_user_by_username_query = "select * from user where username = '%s'"
get_user_by_id_query = "select * from user where id = %s"
register_user_query = "insert into user (name, username, password) values ('%s', '%s', '%s')"
get_tests_query = "select * from tests"
get_test_by_id_query = "select * from tests where id = %s"
get_test_questions_query = "select * from test_questions where test_id = %s"
get_q_answers_query = "select * from test_answers where question_id = %s"
get_results_by_user_query = "select * from test_results where user_id = %s order by play_date desc"
add_results_for_session_query = "insert into test_results (user_id, test_id, score, play_date) values (?, ?, ?, ?)"
update_test_play_count_query = "update tests set play_count = (select count(*) from test_results where test_id = %s) where id = %s"
update_test_avg_score_query = "update tests set average_score = (select avg(tr.score) from test_results tr where test_id = %s) where id = %s"

# логгер sql
def log(message):
    print(f'[SQL] {message}...')

# обёртка для функций sql - проверка на ошибки внутри sql
def sql_error_check(query_function) -> Any:
    def wrapper(*args, **kwargs):
        try:
            return query_function(*args, **kwargs)
        except Error as e:
            if(db): db.rollback()
            return f"Ошибка БД! {' '.join(e.args)}"
        except Exception as e:
            if(db): db.rollback()
            return f"Ошибка! {' '.join(e.args)}"
    return wrapper


# проверка пользователя
@sql_error_check
def validate_credentials(username: str, password: str) -> Any:
    log('Выполняется вход')
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return 'Пользователь не зарегистрован. Перейдите на страницу регистрации'
    else:
        user = User(user_tuple)
        if(user.password == password):
            return user
        else:
            return 'Логин и пароль не совпадают!'


# получение пользователя по id
def get_user_by_id(id: int):
    log('Получение пользователя по id')
    sql.execute(get_user_by_id_query % id)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return None
    else:
        user = User(user_tuple)
        return user


# получение теста по id
def get_test_by_id(id: int):
    log('Получение теста по id')
    sql.execute(get_test_by_id_query % id)
    test_tuple: tuple = sql.fetchone()
    if(test_tuple is None):
        return None
    else:
        test = Test(test_tuple)
        return test


# получение тестов
@sql_error_check
def get_tests() -> list:
    log('Получение списка тестов')
    sql.execute(get_tests_query)
    tests = [Test(test_tuple) for test_tuple in sql.fetchall()]
    return tests


# получение вопросов к тесту
@sql_error_check
def get_test_questions(test_id: int) -> list:
    log(f'Получение вопросов дял теста с id {test_id}')
    sql.execute(get_test_questions_query % test_id)
    questions = [TestQuestion(q_tuple) for q_tuple in sql.fetchall()]
    return questions


# получение ответов на вопрос
@sql_error_check
def get_q_answers(q_id: int) -> list:
    log(f'получение ответов на вопрос с id {q_id}')
    sql.execute(get_q_answers_query % q_id)
    answers = [TestAnswer(answer_tuple) for answer_tuple in sql.fetchall()]
    return answers


# регистрация пользователя
@sql_error_check
def register_user(name: str, username: str, password: str) -> Any:
    log(f'Добавление нового пользователя @{username}')
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is not None):
        return 'Пользователь уже зарегистрирован. Выберете другой логин!'
    
    sql.execute(register_user_query % (name, username, password))
    db.commit()
    set_message('Вы успешно зарегистрировались!')
    go_app('auth_page', new_window=False)


# регистрация результатов теста
@sql_error_check
def register_test_session_results(user_id: int, test_id: int, score: int):
    log(f'Добавление результатов за прохождение теста {test_id}')
    sql.execute(add_results_for_session_query, (user_id, test_id, score, datetime.now()))
    db.commit()
    set_message('Тест пройден!')


# получение результатов пользователя
@sql_error_check
def get_test_results_by_user(user_id: int):
    log(f'Получение таблицы результатов пользователя с id {user_id}')
    sql.execute(get_results_by_user_query % user_id)
    results = [TestResult(result_tuple) for result_tuple in sql.fetchall()]
    return results


# обновление теста после прохождения
@sql_error_check
def update_test_after_play(test_id: int):
    log(f'Обновление теста с id {test_id}')
    sql.execute(update_test_play_count_query % (test_id, test_id))
    sql.execute(update_test_avg_score_query % (test_id, test_id))
    db.commit()