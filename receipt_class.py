import datetime
import phonenumbers


class Receipt:
    def __init__(self, str):
        self.str = str
        self.str_lst = str.split('\n')
        self.date = None
        self.phone = None

    def get_date(self):
        for line in self.str_lst:
            try:
                if line[2] == '/' and line[5] == '/':
                    self.date = line
            except:
                pass

    def get_phone(self):
        for line in self.str_lst:
            line = line.replace(' ', '')
            if '(' and ')' in line:
                try:
                    phone_number = phonenumbers.parse(line, 'US')
                    self.phone = phone_number
                except:
                    pass





