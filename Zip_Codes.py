"""

Getting a dataframe of all lat/long given a zip code

"""
import pandas as pd


# read into a dataframe
df2 = pd.read_csv("US_Zip_Codes.txt")


# add back starting 0s
def zip_fixer(zip):
    """
    :param zip (int): a zipcode
    :return zip (str): a zipcode but as a string and including the starting 0s
    """

    if len(str(zip)) == 3:
        zip = "00" + str(zip)
    elif len(str(zip)) == 4:
        zip = "0" + str(zip)
    elif len(str(zip)) == 5:
        zip = str(zip)

    return zip

# create new zipcodes
results = list(map(zip_fixer, df2['ZIP']))

# replace old zip codes with new ones
df2["ZIP"] = results









