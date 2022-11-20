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
        self.change = None
        self.items = None
        self.costs = None
        self.quantities = None
        self.ids = None

    def get_date(self):
        ''' gets the date of the transaction from the receipt'''
        for line in self.str_lst:
            try:
                if line[2] == '/' and line[5] == '/':
                    self.date = line
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

    def change_due(self):
        '''getting the value associated with change due'''
        for line in self.str_lst:
            if re.search('change', line.lower()):
                self.change = line.lower().strip().split(' ')[-1]

    def get_items(self):
        '''getting the list of items on the receipt and a list of their prices'''
        item_line = []
        item_cost = []
        item_quantity = []
        item_id = []

        for line in self.str_lst:
            split_line = line.strip().split(' ')
            split_line = [val.lower() for val in split_line]
            for item in split_line:
                try:
                    # checking if an item in the line ends in the style '.XX'
                    if item[-3] == '.' and item[-2:-1].isnumeric():
                        # making sure tax, subtotal, change are not in the line
                        if not any(val in ['total','subtotal','tax','change','visa'] for val in split_line):
                            item_cost.append(item)

                            # adding everything before the cost index to the other list
                            idx = split_line.index(item)
                            non_cost_line = split_line[:idx]

                            if split_line[0].isnumeric():
                                item_quantity.append(split_line[0])
                                # removing quantity
                                non_cost_line = non_cost_line[1:]
                            else:
                                item_quantity.append(1)

                            # making sure the last item is not one character before checking if it is an ID
                            if len(non_cost_line[-1]) == 1:
                                non_cost_line = non_cost_line[:-1]

                            # checking for an id
                            if non_cost_line[-1].isnumeric():
                                item_id.append(non_cost_line[-1])
                                item_line.append(non_cost_line[:-1])
                            else:
                                item_id.append(None)
                                item_line.append(non_cost_line)
                except:
                    pass

        self.items = item_line
        self.costs = item_cost
        self.ids = item_id
        self.quantities = item_quantity

    def __str__(self):
        '''updating print statement'''
        return f'Receipt: \nDate - {self.date}\nMerchant Phone Number - {str(self.phone)}\nSubtotal - {self.subtotal}\nTotal - {self.total}\nChange Due - {self.change}'

    def __repr__(self):
        return f'Receipt: \nDate - {self.date}\nMerchant Phone Number - {str(self.phone)}\nSubtotal - {self.subtotal}\nTotal - {self.total}\nChange Due - {self.change}'