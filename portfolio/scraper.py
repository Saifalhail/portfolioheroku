import pandas as pd
from pandas.core import strings
import requests
from bs4 import BeautifulSoup
import pickle
import requests
import random
import re
import os 
from collections import defaultdict
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

# replacer_list = set(["Market Cap (intraday) 5", "Shares Outstanding 5", "Forward Annual Dividend Yield 4", 
#     "Trailing Annual Dividend Yield 3", "Payout Ratio 4", "Profit Margin ", "Return on Assets (ttm)", 
#     "Return on Equity (ttm)"])

def replacer (value):
    new_value = value
    if "T" in new_value and '.' in new_value:
        new_value = value.replace('T', '0000000000')
        new_value = new_value.replace('.', '')
    elif "T" in new_value:
        new_value = value.replace('T', '0000000000000')
    if "B" in new_value and '.' in new_value:
        new_value = value.replace('B', '0000000')
        new_value = new_value.replace('.', '')
    elif "B" in new_value:
        new_value = value.replace('B', '0000000000')
    if "M" in new_value and '.' in new_value:
        new_value = value.replace('M', '0000')
        new_value = new_value.replace('.', '') 
    elif "M" in new_value:
        new_value = value.replace('M', '0000000')
    if "%" in new_value:
        new_value = value.replace('%', '')
    if ',' in new_value:
        new_value = new_value.replace(',','')
    
    try:
        new_value = pd.to_numeric(new_value)
    except:
        pass

    return new_value

def pickles_operator(df, url):
    start = url.find('quote/') + 6
    end = url.find('?p=', start)
    text_path = url[start:end]
    text_path = text_path.replace("/", "_", 1)
    text_path = "./pickles/" + text_path + ".pkl"
    directory = "./pickles"
    isExist = os.path.exists(directory)

    if not isExist:
        os.makedirs(directory)

    df.to_pickle(text_path)
    return df

def convert_to_numeric(column):
    vals = []
    first_col = [i.replace(',','') for i in column]
    for i in range(len(first_col)):
        try:
            final_col = float(first_col[i])
        except:
            final_col = 0
        vals.append(final_col)
    return vals


class start_scraper:
    def __init__(self):
        print('------------------------------Gathering Financials Now------------------------------')
        self.driver = None
    
    """
        @scraper_type can be statistics or normal

    """ 
    
    def extract_statistics(self, url):
        ######## chrome driver scraper
        if self.driver is None:
            self.driver = webdriver.Chrome()
        
        self.driver.get(url)
        time.sleep(1)
        src_page = self.driver.page_source
        soup = BeautifulSoup(src_page, "lxml")
        #### Old scraper
        # user_agent = random.choice(user_agent_list)
        # headers = {'User-Agent': user_agent}
        # response = requests.get(url,headers=headers)
        # time.sleep(1)
        # soup = BeautifulSoup(response.content, 'lxml')
        features = soup.find_all('tr', class_='Bxz(bb)')
        # price_gather = soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        # prices = []
        # for x in price_gather:
        #     prices.append(str(x))
        # price_list = [x.split('>')[1] for x in prices]
        # price = re.sub('[^\d\.]', '', price_list[0])
        
        keys = []
        values = []


        for item in features:
            a = item.find('td', class_='Pos(st)').text
            b = item.find('td', class_='Fw(500)').text
            keys.append(a)
            values.append(b)
        
        stats_dictionary = dict(zip(keys, values))
        # stats_dictionary['Price'] = price
        to_delete = []

        for key in stats_dictionary:
            if stats_dictionary[key] == 'N/A' or stats_dictionary[key] == 'None':
                to_delete.append(key)

        for key in to_delete:
            del stats_dictionary[key]

        for key in stats_dictionary:
            value = stats_dictionary[key]
            stats_dictionary[key] = replacer(value)
        items = stats_dictionary.items()
        df = pd.DataFrame(items)
        pickles_operator(df, url)
        return df


    def extract_financials(self, url):
        # TODO: Check if this is correct
        ######## chrome driver scraper
        # if self.driver is None:
        #     options = Options()
        #     options.add_argument('--headless')
        #     self.driver = webdriver.Chrome(options=options)
        
        # self.driver.get(url)
        # time.sleep(1)
        # src_page = self.driver.page_source
        # soup = BeautifulSoup(src_page, "lxml")
       #### Old scraper
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent }
        
        response = requests.get(url,headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(response.content, 'lxml')

        

        features = soup.find_all('div', class_='D(tbr)')
        stats = []
        temp_list = []
        label_list = []
        final = []
        index = 0
        #create headers
        if len(features) > 0:
            for item in features[0].find_all('div', class_='D(ib)'):
                stats.append(item.text)
        else:
            print(url)
        #statement contents
        while index <= len(features)-1:
            #filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                #each item adding to a temporary list
                temp_list.append(line.text)
            #temp_list added to final list
            final.append(temp_list)
            #clear temp_list
            temp_list = []
            index+=1

        df = pd.DataFrame(final[1:])
        df.columns = stats

        for column in stats[1:]:
            df[column] = convert_to_numeric(df[column])
        pickles_operator(df, url)
        
        # self.driver.quit()
        return df

    # def extract_sectors(self, url):
    #     user_agent = random.choice(user_agent_list)
    #     headers = {'User-Agent': user_agent}

        
    #     response = requests.get(url,headers=headers)
    #     soup = BeautifulSoup(response.content, 'lxml')
    #     features = soup.find_all('span', class_='Fw(600)')
    #     sectors = []
    #     for x in features:
    #         sectors.append(str(x))
    #     sectors2 = [x.split('>')[1] for x in sectors]
    #     s = sectors2[0] + sectors2[1]
    #     start = s.find('') 
    #     second_start = s.find('</span') + 6
    #     end = s.find('</span', start)
    #     second_end = s.find('</span', second_start)
    #     sector = s[start:end]
    #     industry = s[second_start:second_end]
    #     return sector, industry 
    
    def convertStringToVal(self, val):
        real_val = str(val)
        res = real_val.replace(",", "")
        return res


    def extract_profile(self, url):
        ######## chrome driver scraper
        if self.driver is None:
            
            options = Options()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
        
        self.driver.get(url)
        time.sleep(1)
        src_page = self.driver.page_source
        soup = BeautifulSoup(src_page, "lxml")
        ###### Old
        # user_agent = random.choice(user_agent_list)
        # headers = {'User-Agent': user_agent}
        # response = requests.get(url,headers=headers)
        # time.sleep(1)
        # soup = BeautifulSoup(response.content, 'lxml')
        features = soup.find_all('section', class_='quote-sub-section Mt(30px)')
        features2 = soup.find_all('div', class_='asset-profile-container')
        features3 = soup.find_all('span', class_='Fw(600)')

        sectors = []
        description = []
        names = []

        for x in features:
            description.append(str(x))
        for x in features2:
            names.append(str(x))
        for x in features3:
            sectors.append(str(x))

        sectors2 = [x.split('>')[1] for x in sectors]
        s = sectors2[0] + sectors2[1]
        start3 = s.find('') 
        second_start = s.find('</span') + 6
        end3 = s.find('</span', start3)
        second_end = s.find('</span', second_start)
        sector = s[start3:end3]
        industry = s[second_start:second_end]

        start = description[0].rfind('Lh(1.6)') + 28
        end = description[0].find('/section', start) - 5

        start2 = names[0].find('Mb(10px)') + 27
        end2 = names[0].find('Mb(25px)', start2) - 17

        name_info = names[0][start2:end2]
        descriptions = description[0][start:end] # Done here

        dicto = {'Company_Name': name_info, 'Sector':sector, 'Industry': industry, 'Description': descriptions}
        start = url.find('quote/') + 6
        end = url.find('?p=', start)
        text_path = url[start:end]
        text_path = text_path.replace("/", "_", 1)
        text_path = "./pickles/" + text_path + ".pkl"
        directory = "./pickles"
        isExist = os.path.exists(directory)

        if not isExist:
            os.makedirs(directory)

        with open(text_path, 'wb') as handle:
            pickle.dump(dicto, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return dicto

    def extract_growth(self, url):
        ######## chrome driver scraper
        if self.driver is None:
            self.driver = webdriver.Chrome()
        
        self.driver.get(url)
        time.sleep(1)
        src_page = self.driver.page_source
        soup = BeautifulSoup(src_page, "lxml")
        ##### OLD
        # user_agent = random.choice(user_agent_list)
        # headers = {'User-Agent': user_agent}
        # response = requests.get(url,headers=headers)
        # time.sleep(1)
        # soup = BeautifulSoup(response.content, 'lxml')
        features = soup.find_all('td', class_='Ta(end) Py(10px)')
        stats = []

        for x in features:
            stats.append(re.sub('abc', '', x.text))


        new_set = {x.replace('%', '') for x in stats}
        new_set2 = [e for e in new_set if e not in ('N/A')]
        # growth_estimates = [float(k) for k in new_set2]
        growth_estimates = [float(self.convertStringToVal(k)) for k in new_set2]

        dicto = {'Growth': growth_estimates}
        start = url.find('quote/') + 6
        end = url.find('?p=', start)
        text_path = url[start:end]
        text_path = text_path.replace("/", "_", 1)
        text_path = "./pickles/" + text_path + ".pkl"
        directory = "./pickles"
        isExist = os.path.exists(directory)

        growth_rate = {}
        for i in dicto.values():
            if i:
                rate = sum(i) / len(i)
                growth_rate['Growth'] = round(rate, 2)
            else:
                growth_rate['Growth'] = 0

        if not isExist:
            os.makedirs(directory)

        with open(text_path, 'wb') as handle:
            pickle.dump(growth_rate, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return dicto

def run_scraper():
    start = start_scraper()
    a = start.extract_financials(url = 'https://finance.yahoo.com/quote/ORDS.QA/financials?p=ORDS.QA')
    print (a)
    return a