"""
Used in order to identify food categories for different foods using a dataset of foods and their groups and sub groups

 - deal with abbreviations that don't just get rid of vowels
 - look into expanding for more food?
 - lemon dressing
 - what if when you add items that are "other" you can specify a category for them and it updates the directory of food


"""
from itertools import chain, combinations
import pandas as pd

"""
The hard part about reciepts is that sometimes food is abbreviated and not full written out, hopefully
this code can solve part of that issue. ALso if we like it we can just implement it directly into our reciept item
"""



def abbreviations(food):
    """ creates a list of possible abbreviations for a food
    :param food: a string that is the name of a food
    :return abbreviations: a list of possible abbreviations for that food
    """
    # create a list of vowels
    vowel_list = ["a", "e", "i", "o", "u"]

    # pull out all vowels in the word
    vowels = [char for char in food if char in vowel_list]

    # get all combinations of these vowels
    vowel_combos = list(chain.from_iterable(combinations(vowels, r) for r in range(len(vowels) + 1)))

    abbrev_options = []
    for combo in vowel_combos:
        abbrev = food
        for vowel in combo:
            abbrev = abbrev.replace(vowel, "", 1)
        abbrev_options.append(abbrev)

    # deal with any cases where the food is made plural
    plural_food = food + "s"
    abbrev_options.append(plural_food)

    # return the combinations
    return abbrev_options


def group_identify(food_df, food):
    """ find the group for a food

    :param food:
    :return group:
    """

    # make the food lowercase
    food = food.lower()

    # set group to default value
    group = "other"

    # find the foods group
    for index, row in food_df.iterrows():

        # split the food into seperate words
        food_split = food.split()

        if row["FOOD NAME"] in food_split:
            group = row["GROUP"]
            break


        elif any(item in food_split for item in abbreviations(row["FOOD NAME"])):
            group = row["GROUP"]
            break

    # return the group of the food
    return group

def categorize_foods(item_df):
    # create a dataframe for our food catagory data
    food_data = pd.read_csv("generic-food.csv")
    food_data = food_data[["FOOD NAME", "GROUP", "SUB GROUP"]]

    # pull out all food names
    food_names = list(food_data["FOOD NAME"])

    # drop the other in all food names
    new_food_names = list(map(lambda food: food.replace("Other", ""), food_names))

    # get rid of parenthisis in food names
    new_food_names = list(map(lambda food: food.split("(")[0].strip(), new_food_names))

    # makes all foods lowercase
    new_food_names = list(map(lambda food: food.lower(), new_food_names))

    # put food names back into data set, change all to lowercase
    food_data["FOOD NAME"] = new_food_names
    item_df['Category'] = None
    # iterate over the item df
    for ind in item_df.index:
        item_name = item_df['Item_Name'][ind]

        # categorizing each item
        category = group_identify(food_data, item_name)
        item_df['Category'][ind] = category

    return item_df
