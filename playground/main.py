from pywebio.input import NUMBER, file_upload, input, input_group, slider
from pywebio.output import put_code, put_column, put_image, put_row, put_text, use_scope
from pywebio.platform.tornado import start_server


def check_age(p):  # return None when the check passes, otherwise return the error message
    if p < 10:
        return 'Too young!!'
    if p > 60:
        return 'Too old!!'


def main_page():
    put_row([
        put_column([
            put_code('A'),
            put_row([
                put_code('B1'), None,  # None represents the space between the output
                put_code('B2'), None,
                put_code('B3'),
            ]),
            put_code('C'),
        ]), None,
        put_code('D'), None,
    put_code('E')
    ])
   
if __name__ == '__main__':
    #start_server(main_page, debug=True, port=8080, cdn=False)
    main_page()


