# test-site-pywebio - Сайт с тестами на PyWebIO
[![Открыть в среде](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/iCatOK/test-site-pywebio)

Course work for Ufa State Petrolium Technological University, 2021.

## Описание проекта
Проект представляет из себя сайт с тестами с сохранением истории их прохождения. Тесты отображаются на главной странице в виде карточек с картинкой, описанием и основными характеристиками:
- количество прохождений;
- средний балл;
- количество вопросов.

![image](https://user-images.githubusercontent.com/23420574/144195476-b882c83e-8257-4d8e-aecf-62254b3eba8e.png)

Каждый вопрос имеет картинку, текст вопроса и ответы на них. За каждый вопрос дается один балл и в дальнейшем высчитывается сумма баллов.

![image](https://user-images.githubusercontent.com/23420574/144195670-a7552ef4-4742-4847-8c4c-b85174ba8b3b.png)

Пользователь может посмотреть свои результаты в таблице результатов после прохождения теста.

![image](https://user-images.githubusercontent.com/23420574/144195892-30d50514-e027-4241-b689-3c6ef8af551e.png)

## Кодовая база
Весь проект написан с использованием библиотеки PyWebIO на языке Python (а также отдельных библиотек для работы с базами данных и датами). С помощью PyWebIO удалось реализовать:
- авторизация с использованием контрактов к БД;
- использование cookie с помощью javascript-вставок для сохранения авторизации пользователя;
- стилизация отдельных модулей библиотеки PyWebIO;
- добавление интерактивных элементов, такие как кнопки, радиобатоны и поля для ввода.
При этом не было написано ни одной строчки html-кода, библиотека скомпилировала html-страницы на основе Python-кода.

## Некоторые PyWebIO-сниппеты из реализации проекта  
Страница регистрации на PyWebIO:

```python
from pywebio.output import put_buttons, put_column, put_error, put_markdown, put_text
from pywebio.input import NUMBER, PASSWORD, input_group
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from classes.user import User
import classes.user as user_info
from messages import show_message
from cookie_io import get_current_user_id, init_js_cookie_io, is_test_mode, set_cookie
from sql import validate_credentials

# переход на страницу регистрации
def register():
    go_app('register_page', new_window=False)


# вход в систему
def login():
    answer = validate_credentials(pin.username, pin.password)

    if(type(answer) is User):
        set_cookie('current_user_id', f'{answer.id}')
        go_app('test_list_page', new_window=False)
    else:
        put_error(answer, closable=True)


# редирект в случае пойманных куки
def redirect():
    id = get_current_user_id()
    
    if id != None:
        go_app('test_list_page', new_window=False)
    
    if(is_test_mode()):
        go_app('test_play_page', new_window=False)


# основной код страницы авторизации
def auth_page():
    init_js_cookie_io()
    redirect()
    show_message()
    put_markdown('# ✅ Авторизация')
    put_column([
        put_input('username', label='Логин'),
        put_input('password', label='Пароль', type=PASSWORD)
    ])
    put_buttons(['Войти', 'Регистрация'], onclick=[login, register])
```

JS-вставка для работы с cookies:
```python
# инициализация js кода для взаимодействия с куки
def init_js_cookie_io():
    run_js("""
        window.setCookie = function(name,value,days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "") + expires + "; path=/";
        }
        
        window.getCookie = function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }

        window.deleteCookie = function(name) {
            document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        }
        """
    )


# создание переменной
def set_cookie(key, value, days=30):
    run_js("setCookie(key, value, days)", key=key, value=value, days=days)


# получение переменной
def get_cookie(key):
    return eval_js("getCookie(key)", key=key)


# удаление куки
def remove_cookie(key):
    run_js('deleteCookie(key)', key=key)
```

Стилизация модуля с кнопки в PyWebIO (добавление центрирования):

```python
style(put_buttons(['Посмотреть свои результаты', 'Выйти'], [results, logout]), 'align-self: center')
```

Вы можете открыть среду разработки с установленными зависимостями прямо в браузере! Просто нажимте на кнопку ниже.

[![Открыть в среде](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/iCatOK/test-site-pywebio)
