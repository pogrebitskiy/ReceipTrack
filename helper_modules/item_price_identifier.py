import itertools

def find_item_prices(str_lst, total):
    '''To find each item in the receipt and their prices'''
    price_lst = None
    # try to identify items and prices using the
    try:
        price_lst = combination_method(str_lst, total)
        if price_lst:
            return price_lst
    except:
        pass



def combination_method(str_lst, total):
    '''First method to identify items, iterates over different combinations of values in the receipt and matches the sum
     to the total to find a matching set of items'''
    total = float(total)
    item_lst = []
    price_numbers = []
    # iterate over each line in the receipt
    for i in range(len(str_lst)):
        line = str_lst[i]
        # separate each line to different elements
        line_lst = line.split(' ')
        item_name = []
        # iterate over line elements
        for elmt in line_lst:
            # check if element is a pure string
            if elmt.isalpha() and len(elmt) > 1:
                # append to item name
                item_name.append(elmt.upper())
        # join the item name to a string
        item_name = ' '.join(item_name)

        # periods can be confused for commas, so fixing it here
        line_lst = [element.replace(',','.') for element in line_lst]

        # iterate over each element in line
        for elmt in line_lst:
            # check if a period is within element, which could signify a float (item price)
            if '.' in elmt:
                try:
                    # when buying multiple of an item, we do not want to get the price of one item
                    if line_lst[line_lst.index(elmt) - 1] == '@':
                        item_name = []
                        prev_line_lst = str_lst[i-1].split(' ')
                        for elmt in prev_line_lst:
                            if elmt.isalpha() and len(elmt) > 1:
                                item_name.append(elmt.upper())
                        item_name = ' '.join(item_name)
                        continue
                except:
                    pass
                # the ocr may identify '-' as '~', so clean this
                elmt = elmt.replace('~', '-')
                # remove $ symbols
                elmt = elmt.replace('$', '')
                # try to convert element to a float
                try:
                    item_value = float(elmt)
                    # if succesful, check if the float is less than total
                    if item_value < total:
                        # append to list of prices
                        price_numbers.append(item_value)
                        # append to list of items
                        item_lst.append([item_name, item_value])
                except:
                    pass
    # check for a subset of the values that is equal to the total
    item_costs = find_matching_sum(price_numbers, total)
    price_lst = []
    # match the item prices to item names
    for price in item_costs:
        for item in item_lst:
            name = item[0]
            val = item[1]
            if val == price:
                price_lst.append([name, val])
                item_lst.pop(0)
                break
    return price_lst

def find_matching_sum(number_lst, total):
    '''Use combinations to find a subset that has a sum equal to the total'''
    if sum(number_lst) == total:
        return set(number_lst)

    for L in reversed(range(len(number_lst))):
        for subset in itertools.combinations(number_lst, L):
            if sum(subset) == total:
                item_costs = subset
                return item_costs

