import pandas as pd 
import csv 

user_input = input("Choose Company Ticker: ")

def filename(file):
    prices = []
    df3 = pd.read_csv(file)
    df4 = pd.DataFrame(df3)
    closing_prices = df4.iloc[0: , 4]
    vals = closing_prices.values
    last_closing_price = vals.tolist()[-1]
    prices.append(last_closing_price)
    first_closing_price = vals.tolist()[0]
    prices.append(first_closing_price)
    return prices

def filename2(file):
    df3 = open(file)
    reader_file = csv.reader(df3)
    value = len(list(reader_file))
    return value

length = filename2("extract_financials/prices{}.QA.csv".format(user_input))
years = length / 263
last_price = filename("extract_financials/prices{}.QA.csv".format(user_input))[0]
first_price = filename("extract_financials/prices{}.QA.csv".format(user_input))[1]
