import random


def generate_id(data):
    id = ''
    symbols = '1234567890'
    for i in range(6):
        id += random.choice(symbols)
    for cell in data:
        if cell.value == id:
            generate_id(data)
    return id

def is_unique_phone(data, phone):
    for cell in data:
        if cell.value ==  phone:
            return False   
        
    return True