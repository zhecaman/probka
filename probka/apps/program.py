import PySimpleGUI as sg
from helpers import validate_phone, generate_idcode
from db import BotDB
import time


layout = [
    [sg.Text('Генератор уникального ID для конкурса')],
    [sg.Text('Код:'), sg.Text(key='-OUTPUT-')],
    [sg.Text('Введите номер телефона гостя: '), sg.Input(key='-IN-', enable_events=True, size=11)],
    [sg.Text('', font=('italic', 11), key='-OK-')],
    [sg.Button('Сгенерировать', enable_events=True), sg.Button('Сохранить', disabled=True, key='-SAVE-')],
    ]

            
window = sg.Window('PROBKA', layout)


while True:
    database = BotDB('probka.db')
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, None):
        break
    if event == 'Сгенерировать':
        window['-OK-'].Update('')
        id_code = generate_idcode()
        phone_num = window['-IN-'].get()
        time.sleep(0.3)
        window['-OUTPUT-'].Update(value=id_code)
        window['-SAVE-'].Update(disabled=False)
        try:
            if validate_phone(phone_num):

                if database.user_exists_phone(phone_num):
                    sg.popup_error('Этот номер уже учавствует в розыгрыше!')
                    window['-IN-'].Update('')
                    window['-OUTPUT-'].Update('')
                database.add_phone_and_code(f'7{phone_num[1:]}', id_code)
            else:
                sg.popup_error('Это не похоже на номер телефона.')
            
        except Exception as e:
            sg.popup_error(f'Что-то пошло не так :(  {e}')

    if event == '-SAVE-':
        try:
            if phone_num:
                window['-OK-'].Update('Запись добавлена в таблицу')
            
                window['-OUTPUT-'].Update('')
                window['-IN-'].Update('')
            else:
                window['-OK-'].Update('Невозможно добавить запись. Вы не ввели номер телефона.')
        except Exception as e:
            sg.popup_error(f'Возникла ошибка: {e}')
        window['-SAVE-'].Update(disabled=True)
        database.close()
window.close()