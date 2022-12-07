import re
from helper_modules.phone_identifier import find_phonenumber
from helper_modules.item_price_identifier import find_item_prices
import pandas as pd
from helper_modules.Food_Identification import categorize_foods
import pytesseract
import cv2


def read_receipt(filepath):
    """
    Function that reads in a file from a path into a receipt object by calling its constructor

    Code used to find tesseract on Windows, specific to Jacob
    pytesseract.pytesseract.tesseract_cmd = r"C:/Users/jakul/anaconda3/Library/bin/tesseract.exe"

    """

    img = cv2.imread(filepath, 0)
    # configurations
    config = '-l eng --oem 1 --psm 6'

    # Parse text using pytesseract
    text = pytesseract.image_to_string(img, config=config, lang='eng')

    # Create a Receipt object using the parsed text
    return Receipt(text)


class Receipt:
    def __init__(self, init_str):
        '''constructor'''
        # setting up all attributes
        self.str = init_str
        self.str_lst = init_str.split('\n')
        self.date = None
        self.phone = None
        self.subtotal = None
        self.total = None
        self.change = None
        self.items = None
        self.costs = None
        self.quantities = None
        self.ids = None
        self.item_lst = None
        self.identification_lst = None
        self.category_dct = None

        # gets the date of the transaction from the receipt
        for line in self.str_lst:
            if '/' in line:
                for idx in range(len(line)):
                    try:
                        if line[idx:idx + 2].isnumeric() and line[idx + 2] == '/' and line[idx + 5] == '/':
                            if line[idx + 8].isnumeric() and line[idx + 9].isnumeric():
                                self.date = line[idx:idx + 10]
                            else:
                                self.date = line[idx:idx + 8]
                    except:
                        pass

        # gets the phone number associated with the receipt
        phone = find_phonenumber(self.str_lst)
        self.phone = phone

        # getting the subtotal and total of the receipt
        for line in self.str_lst:
            # using the regex search function to narrow down to the proper lines
            if re.search('total', line.lower()):
                if re.search('sub', line.lower()):
                    line_amnt = line.lower().replace('total', '').replace('sub', '').replace(' ', '').strip()
                    self.subtotal = re.sub(r'[^(0-9|.]', '', line_amnt)
                else:
                    line_amnt = line.lower().replace('total', '').replace(' ', '').strip()
                    self.total = re.sub(r'[^(0-9|.)]', '', line_amnt)

        # getting the value associated with change due
        for line in self.str_lst:
            if re.search('change', line.lower()):
                self.change = line.lower().strip().split(' ')[-1]

        # getting the list of items on the receipt and a list of their prices
        item_line = []
        item_cost = []
        item_quantity = []
        item_id = []

        # getting the phone number from the list of strings
        for line in self.str_lst:
            split_line = line.strip().split(' ')
            split_line = [val.lower() for val in split_line]
            for item in split_line:

                try:
                    # checking if an item in the line ends in the style '.XX'
                    if (item[-3] == '.' and item[-2:-1].isnumeric()) or (
                            item.isnumeric() and len(split_line[split_line.index(item) + 1]) == 2):
                        # making sure tax, subtotal, change are not in the line
                        if not any(val in ['total', 'subtotal', 'tax', 'change', 'visa'] for val in split_line):
                            if '.' in item:
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

                            # print(non_cost_line)
                            # checking for an id
                            if non_cost_line[-1].isnumeric():
                                item_id.append(non_cost_line[-1])
                                item_line.append(non_cost_line[:-1])
                            else:
                                item_id.append(None)
                                item_line.append(non_cost_line)

                except:
                    pass

        # defining test attributes with our lists
        self.items = item_line
        self.costs = item_cost
        self.ids = item_id
        self.quantities = item_quantity

        # working on the list of items more closely, testing the whole list of strings on our total value to find a
        # subset of items that add up correctly
        price_item_lst = find_item_prices(self.str_lst, self.total)

        # creating a dataframe useful for plotting and keeping the data more uniform
        self.item_lst = price_item_lst
        self.item_df = pd.DataFrame(data=price_item_lst, columns=['Item_Name', 'Price'])

        # attempting to categorize foods, will not work on all receipts
        try:
            self.item_df = categorize_foods(self.item_df)
        except:
            pass

        # if the item dataframe has categories, finding the sums of items in the categories
        if len(self.item_df.columns) == 3:
            self.category_dct = {}
            for i in range(len(self.item_df)):
                cur_cat = self.item_df.loc[i, 'Category']
                if cur_cat in self.category_dct:
                    self.category_dct[cur_cat] += self.item_df.loc[i, 'Price']
                else:
                    self.category_dct[cur_cat] = self.item_df.loc[i, 'Price']

    def __str__(self):
        '''updating print statement'''
        return f'Receipt: \nDate - {self.date}\nMerchant Phone Number - {str(self.phone)}\nSubtotal - {self.subtotal}\nTotal - {self.total}\nChange Due - {self.change}\nNumber of items - {len(self.items)}'

    def __repr__(self):
        return f'Receipt: \nDate - {self.date}\nMerchant Phone Number - {str(self.phone)}\nSubtotal - {self.subtotal}\nTotal - {self.total}\nChange Due - {self.change}\nNumber of items - {len(self.items)}'
