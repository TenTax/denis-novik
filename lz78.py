# выполнено на основе https://github.com/DyakoVlad/python-LZ78

def encode(text_from_file):
    dict_of_codes = {text_from_file[0]: '1'}
    encoded_text  = '0' + text_from_file[0]
    text_from_file = text_from_file[1:]
    combination = ''
    code = 2
    for char in text_from_file:
        combination += char
        if combination not in dict_of_codes:
            dict_of_codes[combination] = str(code)
            if len(combination) == 1:
                encoded_text += '0' + combination
            else:
                encoded_text += dict_of_codes[combination[0:-1]] + combination[-1]
            code += 1
            combination = ''
    return encoded_text

def decode(text_from_file):
    dict_of_codes = {'0': '', '1': text_from_file[1]}
    decoded_text = str(dict_of_codes['1'])
    text_from_file = text_from_file[2:]
    combination = ''
    code = 2
    for char in text_from_file:
        if char in '1234567890':
            combination += char
        else:
            dict_of_codes[str(code)] = dict_of_codes[combination] + char
            decoded_text += str(dict_of_codes[combination] + char)
            combination = ''
            code += 1
    return decoded_text
