import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import sqlite3 as db
import time
import datetime

n = 0

# while the election is not over:
while datetime.date.today().timetuple().tm_yday < datetime.date(2020,11,3).timetuple().tm_yday:

    
    #get the webpage
    url = 'https://www2.montgomerycountymd.gov/mcgportalapps/ElectionLocation.aspx?EarlyVoting=1&flag=1'
    r = re.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    #find the html table
    table = soup.find('table')
    
    #convert html table to pandas dataframe
    df = pd.read_html(str(table))[0]
    
    #fix time stamp formatting
    df['timestamp'] = time.time()

    #connect to DB and write dataframe to DB
    con = db.connect('scrape_db.db')
    df.to_sql(name='scrape',con=con , if_exists = 'append')

    #print success and the increment number
    print('success: ' + str(n) + ' at ' + str(datetime.datetime.today()))
    
    #increase the increment
    n = n + 1
 
    #wait 5 minutes (5x60 seconds)
    time.sleep(5*60)

print("the election is over")