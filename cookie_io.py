from pywebio.session import eval_js, run_js


# литералы для сохранения переменных куки
current_user_id = 'current_user_id'
current_test_id = 'current_test_id'
state = 'state'

# список литералов
literals = [
    current_user_id,
    current_test_id,
    state
]


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


# сохранить id пользователя в куки
def save_current_user_id(id: int):
    set_cookie(current_user_id, f'{id}')


# получить id пользователя из куки
def get_current_user_id():
    id = get_cookie(current_user_id)
    return None if id == None or id == '' else int(id)


# удалить информацию о пользователе
def remove_user_info():
    remove_cookie(current_user_id)


# сохранить id текущего теста в куки
def save_current_test_id(id: int):
    set_cookie(current_test_id, f'{id}')


# получить id теста из куки
def get_current_test_id() -> int:
    id = get_cookie(current_test_id)
    return None if id == None or id == '' else int(id)


# удалить информацию о текущем тесте
def remove_test_info():
    remove_cookie(current_test_id)


# удалить все куки
def remove_all_cookies():
    for literal in literals:
        remove_cookie(literal)


# состояние теста
def set_test_mode():
    set_cookie(state, f'test')


# состояние свободное
def set_free_mode():
    set_cookie(state, 'free')


# какое сейчас состояние
def is_test_mode():
    gotten_mode = get_cookie(state)
    return gotten_mode == 'test'


