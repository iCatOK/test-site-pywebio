from pywebio.platform import start_server
from pywebio.output import put_link, put_text, put_buttons
from pywebio.session import defer_call, go_app

from auth import auth_page
from results import results_page
from test_list import test_list_page
from register import register_page
from test_walkthrough import test_play_page
from cookie_io import init_js_cookie_io, remove_all_cookies


# главная страница сайта - редирект на страницу авторизации
def index():
    init_js_cookie_io()
    go_app('auth_page', new_window=False)


# основные модули сайта
main_router = [
    index,
    register_page,
    auth_page,
    test_list_page,
    test_play_page,
    results_page
]


# запуск сайта
start_server(main_router, port=8080, debug=True)