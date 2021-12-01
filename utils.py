from pywebio.output import put_markdown, put_row, put_text, style
from pywebio.session import eval_js, go_app, run_js
from styles import *
import classes.user as user_info


# инициализация js кода для взаимодействия с куки
def init_js_popups():
    run_js("""
        window.getConfirm = function(title) {
            return confirm(title)
        }
        """
    )


def run_after_ok_popup(title):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('попаааап', title)
            ok = eval_js("getConfirm(key)", key=title)
            print(ok)
            if ok == 'true':
                func(*args, **kwargs)
        return wrapper
    return decorator
        


def multi_markdown_text(*lines):
    multi_str = ''
    for line in lines:
        multi_str += line + '\n'
    print(multi_str)
    return put_markdown(lines)


def put_empty_row():
    return put_row([put_text(' ')])


def styled(style_str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return style(func(*args, **kwargs), style_str)
        return wrapper
    return decorator


def login_required(func):
    def wrapper(*args, **kwargs):
        if(user_info.current_user == None):
            print(user_info.current_user)
            go_app('auth_page', new_window=False)
        func(*args, **kwargs)
    return wrapper


def centered_container(output):
    return style(output, test_list_container_style)


def test_cell_container(output):
    return style(output, test_cell_container_style)