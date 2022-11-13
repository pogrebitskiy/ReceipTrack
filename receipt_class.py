import datetime
import phonenumbers
import re

class Receipt:
    def __init__(self, str):
        '''constructor'''
        self.str = str
        self.str_lst = str.split('\n')
        self.date = None
        self.phone = None
        self.subtotal = None
        self.total = None

    def get_date(self):
        ''' gets the date of the transaction from the receipt'''
        for line in self.str_lst:
            try:
                if line[2] == '/' and line[5] == '/':
                    self.date = line
                    print(line)
            except:
                pass

    def get_phone(self):
        '''gets the phone number associated with the receipt'''
        for line in self.str_lst:
            for item in line.split(' '):
                line = item.replace(' ', '')
                if '(' and ')' in line:
                    try:
                        phone_number = phonenumbers.parse(line, 'US')
                        if phonenumbers.is_possible_number(phone_number):
                            if len(line) > 9:
                                self.phone = phone_number
                    except:
                        pass
                elif len(line.split('-')[0]) == 3:
                    try:
                        phone_number = phonenumbers.parse(line, 'US')
                        if phonenumbers.is_possible_number(phone_number):
                            if len(line) > 9:
                                self.phone = line
                    except:
                        pass

    def get_totals(self):
        '''getting the subtotal and total of the receipt'''
        for line in self.str_lst:
            # using the regex search function to narrow down to the proper lines
            if re.search('total', line.lower()):
                if re.search('sub', line.lower()):
                    line_amnt = line.lower().replace('total', '').replace('sub', '').replace(' ', '').strip()
                    self.subtotal = line_amnt
                else:
                    line_amnt = line.lower().replace('total', '').replace(' ', '').strip()
                    self.total = line_amnt