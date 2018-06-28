from bs4 import BeautifulSoup
from mysql.connector import errorcode
from urllib.request import urlopen

import mysql.connector
from env import config

quote_page = 'https://www.exchangerates.org.uk/Nigerian-Naira-NGN-currency-table.html'

try:
    cnx = mysql.connector.connect(**config)
    curA = cnx.cursor(buffered=True)
    # Insert Query
    # query = ("INSERT INTO `CurrencyExchange`(`curr_name`, `naira_value`) VALUES (%s, %s)")
    # Update
    query = ("UPDATE `CurrencyExchange` SET `naira_value`=%s WHERE `curr_name`=%s")

    # query the website and return the html to page
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html5lib')

    naira_table = soup.select("table.currencypage-mini")[1]
    data = naira_table.find_all('tr')

    for tr in data:
        result = []
        for td in tr:
            result.append(str(td.string).strip())
        # print(result)
        curr_name = result[3][4:]
        ngn_val = round(1/float(result[7]), 2)
        curA.execute(query, (ngn_val, curr_name))
        print("Updated", curr_name, "to", ngn_val)
        
        cnx.commit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

else:
    cnx.close()
