import PySimpleGUI as sg
import  openpyxl
from helpers import generate_id, is_unique_phone



layout = [
    [sg.Text('Генератор уникального ID для конкурса')],
    [sg.Text('Код:'), sg.Text(key='-OUTPUT-')],
    [sg.Text('Введите номер гостя: '), sg.Input(key='-IN-', enable_events=True, size=11)],
    [sg.Text('', font=('italic', 11),key='-OK-')],
    [sg.Button('Сгенерировать', enable_events=True), sg.Button('Сохранить')],
    ]

            
window = sg.Window('PROBKA', layout)

book = openpyxl.load_workbook('/mnt/c/Users/Yevhenii/Documents/probka.xlsx')
sheet = book['DUB']

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, None):
        break
    elif event == 'Сгенерировать':
        id_data = sheet['A']
        phone_data = sheet['B']
        id = generate_id(id_data)
        phone_num = window['-IN-'].get()
        window['-OUTPUT-'].Update(value=id)
        try:
            if not phone_num:
                sg.popup_error('Введите номер телефона')
                window['-OK-'].Update('')
            if is_unique_phone(phone_data, phone_num):

                sheet.append([id, phone_num])
                window['-OK-'].Update('Запись добавлена в таблицу')
            else:
                sg.popup_error('Этот номер уже учавствует в розыгрыше!')
                
        except Exception as e:
            sg.popup_error(f'Что-то пошло не так :(  {e}')
    elif event == 'Сохранить':
        try:
            book.save('/mnt/c/Users/Yevhenii/Documents/probka.xlsx')
            window['-OUTPUT-'].Update('')
            window['-IN-'].Update('')
            window['-OK-'].Update('')
        except PermissionError:
            sg.popup_error('Похоже, у тебя открыт файл с данными. Закрой его, пожалуйста.')

window.close()