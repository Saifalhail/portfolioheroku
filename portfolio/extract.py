import pandas as pd
import re
import pickle
import os.path
import urllib.parse
from os.path import exists
import scraper
# from dotenv import load_dotenv
# load_dotenv()
# from prices import stocksPrices

scraper = scraper.start_scraper()

def retrieve_data(user_input):
    user_cash_flow = ("./pickles/{}_cash-flow.pkl".format(user_input))
    user_financials = ("./pickles/{}_financials.pkl".format(user_input))
    user_balance_sheet = ("./pickles/{}_balance-sheet.pkl".format(user_input))
    user_stats = ("./pickles/{}_key-statistics.pkl".format(user_input))
    user_price = ("./pickles/{}_history.pkl".format(user_input))
    user_profile = ("./pickles/{}_profile.pkl".format(user_input))
    user_growth = ("./pickles/{}_analysis.pkl".format(user_input))

    if not exists(user_cash_flow):
        cash_flow_extract = scraper.extract_financials(
            'https://finance.yahoo.com/quote/{0}/cash-flow?p={0}'.format(user_input))
    else:
        cash_flow_extract = pd.read_pickle("./pickles/{}_cash-flow.pkl".format(user_input))
    
    if not exists(user_financials):
        financials_extract = scraper.extract_financials(
            'https://finance.yahoo.com/quote/{0}/financials?p={0}'.format(user_input))
    else:
        financials_extract = pd.read_pickle("./pickles/{}_financials.pkl".format(user_input))

    if not exists(user_balance_sheet):
        balance_sheet_extract = scraper.extract_financials(
           'https://finance.yahoo.com/quote/{0}/balance-sheet?p={0}'.format(user_input))
    else:
        balance_sheet_extract = pd.read_pickle("./pickles/{}_balance-sheet.pkl".format(user_input))

    if not exists(user_stats):
        stats_extract = scraper.extract_statistics(
            'https://finance.yahoo.com/quote/{0}/key-statistics?p={0}'.format(user_input))
    else:
        stats_extract = pd.read_pickle("./pickles/{}_key-statistics.pkl".format(user_input))

    if not exists(user_price):
        price_extract = stocksPrices('{}'.format(user_input), days_back=4800).get_quote()
    else:
        price_extract = pd.read_pickle("./pickles/{}_history.pkl".format(user_input))

    if not exists(user_profile):
        profile_extract = scraper.extract_profile(
           'https://finance.yahoo.com/quote/{0}/profile?p={0}'.format(user_input))
    else:
        with open('./pickles/{}_profile.pkl'.format(user_input), 'rb') as handle:
            profile_extract = pickle.load(handle)

    if not exists(user_growth):
        growth_extract = scraper.extract_growth('https://finance.yahoo.com/quote/{0}/analysis?p={0}'.format(user_input))
    else:
        with open('./pickles/{}_analysis.pkl'.format(user_input), 'rb') as handler:
            growth_extract = pickle.load(handler)

    # cash_flow_extract.append
    cash_flow = cash_flow_extract.set_index('Breakdown').T.to_dict('list')
    # cash_flow.update(growth)
    financials = financials_extract.set_index('Breakdown').T.to_dict('list')

    if 'Breakdown' in balance_sheet_extract:
        balance_sheet = balance_sheet_extract.set_index('Breakdown').T.to_dict('list')
    else:
        balance_sheet = balance_sheet_extract.T.to_dict('list')

    stats_extract0 = stats_extract.set_axis(['Breakdown', 'Values'], axis=1)
    stats = stats_extract0.set_index('Breakdown').T.to_dict('list')
    price =  price_extract.set_index('Date').T.to_dict('list')
    # print ('--------------------DONE ------------------------')
    return cash_flow, financials, balance_sheet, stats, price, profile_extract, growth_extract


cash_flow, financials, balance_sheet, stats, price, profile_extract, growth_extract = retrieve_data(user_input = input("Choose Company Ticker: "))


print (price)
#NDAQ