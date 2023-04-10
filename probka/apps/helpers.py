import re, random




def validate_phone(text):
    regex = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    result = re.match(regex, text)
    return False if result is None or result.group() != text or len(text) < 11 else True

def generate_idcode():
        '''Generate an id for user'''
        id_code = ''
        symbols = '1234567890'
        for i in range(6):
            id_code += random.choice(symbols)
        
        return id_code
        