import os
from numpy.core.numeric import outer
import pandas as pd
import numpy as np

def run_ai(pickle_file):
    # read pickle files
    import_balance_sheet = pd.read_pickle(os.getcwd() + "/portfolio/nn_pickles/balance_sheet_nn.pkl")
    import_cash_flow = pd.read_pickle(os.getcwd() + "/portfolio/nn_pickles/cash_flow_nn.pkl")
    import_financials = pd.read_pickle(os.getcwd() + "/portfolio/nn_pickles/financials_nn.pkl")
    import_price = pd.read_pickle(os.getcwd() + "/portfolio/nn_pickles/price_nn.pkl")
    import_stats = pd.read_pickle(os.getcwd() + "/portfolio/nn_pickles/stats_nn.pkl")

    num_years = 5
    #Features
    df_balance_sheet = pd.DataFrame((k, v) for k, v in import_balance_sheet.items()) ### This has sometimes 3 or 4 years always the missing year is 2021
    df_cash_flow = pd.DataFrame([(k, v) for k, v in import_cash_flow.items()]) ### This always has 4
    df_financials = pd.DataFrame([(k, v) for k, v in import_financials.items()]) ## This always has 4

    df_stats = pd.DataFrame((k, v) for k, v in import_stats.items())
    df_price = pd.DataFrame([(k, v) for k, v in import_price.items()]) # Target
    df_price_2 = df_price[(df_price[0]=="2021-09-30") | (df_price[0]=="2020-09-30") | (df_price[0]=="2019-09-30") | (df_price[0]=="2018-09-28") | (df_price[0]=="2017-09-28")]

    """ 
    The following dataframe stores five years of data from 2017 to 2021
    """

    df_balance_sheet[1] = df_balance_sheet[1].apply(lambda x: [[sub_list[0]]*(num_years-len(sub_list)) + sub_list if len(sub_list) < num_years else sub_list for sub_list in x])
    df_cash_flow[1] = df_cash_flow[1].apply(lambda x: [[sub_list[0]]*(num_years-len(sub_list)) + sub_list if len(sub_list) < num_years else sub_list for sub_list in x])
    df_financials[1] = df_financials[1].apply(lambda x: [[sub_list[0]]*(num_years-len(sub_list)) + sub_list if len(sub_list) < num_years else sub_list for sub_list in x])
    df_stats[1] = df_stats[1].apply(lambda x: [[sub_list[0]]*(num_years-len(sub_list)) + sub_list if len(sub_list) < num_years else sub_list for sub_list in x])
    #df_price_2[1] = df_price_2[1].apply(lambda x: [sub_list[:5] if len(sub_list) == 6 else sub_list for sub_list in x])

    # TODO - separate dataframe that will be fed to a separate NN
    stats = df_stats[1].apply(pd.Series).T
    stats['price'] = None

    FEATURES_TO_DROP = [
        'Total Equity Gross Minority Interest', 'Capital Lease Obligations', 'Treasury Shares Number',
        'Net Tangible Assets', 'Preferred Stock Equity', 'Preferred Shares Number'
        'Income Tax Paid Supplemental Data', 'Preferred Shares Number', 'Income Tax Paid Supplemental Data',
        'Working Capital', 'Invested Capital', 'Tangible Book Value', 'Net Debt',
        'Share Issued', 'Ordinary Shares Number', 'Interest Paid Supplemental Data',
        'Issuance of Capital Stock', 'Repayment of Debt', 'Repurchase of Capital Stock',
        'Net Non Operating Interest Income Expense', 'Other Income Expense',
        'Tax Provision', 'Net Income Common Stockholders', 'Diluted NI Available to Com Stockholders',
        'Basic EPS', 'Basic Average Shares', 'Diluted Average Shares', 'Total Operating Income as Reported',
        'Normalized Income', 'Net Income from Continuing & Discontinued Operation', 'Interest Income',
        'Interest Expense', 'Net Interest Income', 'EBIT', 'Reconciled Cost of Revenue',
        'Net Income from Continuing Operation Net Minority Interest', 'Normalized EBITDA',
        'Tax Rate for Calcs', 'Tax Effect of Unusual Items', 'Total Unusual Items Excluding Goodwill',
        'Total Unusual Items', 'Earnings from Equity Interest Net of Tax', 'Average Dilution Earnings',
        'Rent Expense Supplemental', 'Special Income Charges', 'Credit Losses Provision',
        'Non Interest Expense', 'INTEREST_INCOME_AFTER_PROVISION_FOR_LOAN_LOSS', 'Total Money Market Investments'
    ]
    NUM_COMPANIES = df_balance_sheet[1].apply(pd.Series).shape[1]
    YEARS = ['2021-09-30', '2020-09-30', '2019-09-30', '2018-09-28', '2017-09-28']

    #df_price indicates only 6 companies in 2018, so I retained only 6 companies in other years as well and truncated remaining companies
    df_p = df_price_2.set_index(0)
    min_company = [len(i) for i in df_p[1]]

    df_p = df_p.apply(lambda x : [sublist[:min(min_company)] for sublist in x])

    company_data = {}
    for company_id in range(min(min_company)):  # for each company
        company_data[company_id] = {}
        for k, df in enumerate([df_balance_sheet, df_cash_flow, df_financials]):  # for each df

            # filter out unnecessary rows
            df = df[~df[0].isin(FEATURES_TO_DROP)].reset_index(drop=True)
            company_data[company_id][f'df_{k}'] = {}
            
            company = df[1].apply(pd.Series)[company_id]  # < change this to change the company
            company_df = pd.DataFrame({
                'feature': df[0],
                'company_data': company}
            )
            year_wise_company_df = company_df['company_data'].apply(pd.Series)
            year_wise_company_df.columns = YEARS
            year_wise_company_df['feature'] = company_df['feature']
            year_wise_company_df.set_index('feature', inplace=True)

            features_and_target = []

            
            for year in year_wise_company_df.columns:
                features_for_year = year_wise_company_df[year]
                targets_for_company = df_p.loc[year, :].apply(pd.Series)[company_id] # < -change the company id

                price_inputs = []
                for i in range(6):
                    if i == 3:
                        target = targets_for_company[1][i]  # because the 4 th element is the target
                    else:
                        # price_inputs.append(targets_for_company[1][i])
                        pass

                if k == 2:  # only three data sets are supported, only the last one will add the target
                    all_data = features_for_year.values.tolist() + price_inputs + [target]
                else:
                    all_data = features_for_year.values.tolist() + price_inputs

                features_and_target.append(all_data)

                company_data[company_id][f'df_{k}'][year] = all_data
                
        # company_data[company_id].append(features_and_target.copy())
        
    time_keys = YEARS

    all_features = []
    for company_id in company_data.keys():
        company_features = []
        for year in time_keys:
            try:
                feature_set = []
                for i in range(3): # number of data suorces
                    # print(len(company_data[company_id][f'df_{i}'][year]))
                    feature_set.append(company_data[company_id][f'df_{i}'][year].copy())
                feature_sets = [item for sublist in feature_set for item in sublist]  # flatten
                
                company_features.append(feature_sets)
                # print(len(feature_set), len(feature_sets), len(company_features))
            except:
                pass
        all_features.append(company_features.copy())    
        #pystar1007

    d = []
    for i in all_features:
        for j in i:
            d.append(j.copy())
    final_df = pd.DataFrame(d)
    final_df.to_pickle(os.getcwd() + "/portfolio/rf_pickles/rf_pickle_data_manipulation.pkl")
    print (final_df)
    return final_df

