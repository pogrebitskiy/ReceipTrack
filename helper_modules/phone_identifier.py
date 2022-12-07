import phonenumbers
import string

def find_phonenumber(string_lst):
    phone = None
    for line in string_lst:
        try:
            phone = phone_method1(line)
            if phone != None:
                return phone
        except:
            pass
        try:
            phone = phone_method2(line)
            if phone != None:
                return phone
        except:
            pass
        try:
            phone = phone_method3(line)
            if phone != None:
                return phone
        except:
            pass


def phone_method1(line):
    line = line.replace(' ', '')
    if '(' and ')' in line:
        phone_number = phonenumbers.parse(line, 'US')
        if phonenumbers.is_possible_number(phone_number):
            if len(line) > 9:
                phone = line
                return phone

def phone_method2(line):
    line = line.replace(' ', '')
    if len(line.split('-')[0]) == 3:
        phone_number = phonenumbers.parse(line, 'US')
        if phonenumbers.is_possible_number(phone_number):
            if len(line) > 9:
                phone = line
                return phone

def phone_method3(line):
    line_lst = line.split(' ')
    for item in line_lst:
        if '(' and ')' in item:
            phone = phone_method1(item)
            return phone
        elif '-' in item:
            phone = phone_method2(item)
            return phone
