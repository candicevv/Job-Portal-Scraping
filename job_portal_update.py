import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\chen2\client_secret.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Career Future").sheet1
n_row=len(wks.col_values(1))

import unittest
from selenium import webdriver
import unicodecsv as csv
import time
from datetime import timedelta
import datetime
import math
import pandas as pd
import codecs
import sys
import datetime

now = datetime.datetime.now()
wks.resize(n_row)


for j in range(0,100):
    driver = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver")
    # get the url
    url = "https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=" + str(j)
    driver.get(url)
    time.sleep(5)
    last_post=driver.find_elements_by_name("last_posted_date")
    last=last_post[len(last_post)-2].text
    label = 1
    if (last=='Posted today'):
        label = 0

    company=driver.find_elements_by_name("company")
    job_title=driver.find_elements_by_name("job_title")
    location=driver.find_elements_by_name("location")
    employment_type=driver.find_elements_by_name("employment_type")
    seniority=driver.find_elements_by_name("seniority")
    category=driver.find_elements_by_name("category")
    salary=driver.find_elements_by_class_name("lh-solid")
    number=len(company)
    for k in range(len(location)):
            location[k]=location[k].text
    for k in range(len(employment_type)):
            employment_type[k]=employment_type[k].text
    for k in range(len(seniority)):
            seniority[k]=seniority[k].text
    if (len(location)<number*2):      
        info=driver.find_elements_by_name("job_info")
        place=["East","South","West","North","Central","Islandwide"]
        for u in range(number):
            inf=info[u*2].text
            if not any(ext in inf for ext in place):
                location.insert(u*2,"missing")
                location.insert(u*2+1,"missing")


    if (len(seniority)<number*2):
        info=driver.find_elements_by_name("job_info")
        senior=["xecutive","Professional","Senior","Manager","Management","entry level"]
        for u in range(number):
            inf=info[u*2].text
            if not any(ext in inf for ext in senior):
                seniority.insert(u*2,"missing")
                seniority.insert(u*2+1,"missing")

    if (len(employment_type)<number*2):
        info=driver.find_elements_by_name("job_info")
        empl=["Perman","Full","Part","Contract","Flexi","Tempor"]
        for u in range(number):
            inf=info[u*2].text
            if not any(ext in inf for ext in empl):
                employment_type.insert(u*2,"missing")
                employment_type.insert(u*2+1,"missing")

    for i in range(number*3):
        try:
            salary[i]=salary[i].text
            if (salary[i]=="Salary undisclosed"):
                salary.insert(i+2,"missing")
            elif("$" in salary[i]):
                if ("to" not in salary[i]):
                    salary.insert(i+1,"missing")
        except:
            pass
    
    for i in range(number):
        company_info=[now.strftime("%Y-%m-%d"),company[i].text,job_title[i].text,location[i*2],employment_type[i*2],seniority[i*2],category[i*2].text,salary[3*i],salary[3*i+2]]
        wks.append_row(company_info)
        time.sleep(1)


    driver.quit()
    if (label == 1):
        print("Page" + str(i) + "Not Today")
        exit()

