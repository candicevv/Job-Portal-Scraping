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
import re

now = datetime.datetime.now()
wks.resize(n_row)

print("Please Select the day do you want to scrape?")
number=input("1 - Yesterday | 2 - Today | 3 - Input Date Range ")
start_page = 0

if number=="3":
    print("Please input the range you want to scrape. Attention: Please ignore 0 at the beginning of each number")
    start = input("Start from(YYYY-M-D): ")#Input here is a string
    end = input("End at(YYYY-M-D): ")
    start=str(start)
    end=str(end)
    start_date=datetime.datetime.strptime(start, '%Y-%m-%d').date()#convert string input to date
    end_date=datetime.datetime.strptime(end, '%Y-%m-%d').date()
    s_diff=now.date()-start_date
    if (s_diff.days == 0):
        s_diff = "today"
    elif (s_diff.days == 1):
        s_diff = "yesterday"
    else:
        s_diff=str(s_diff.days)+" days ago"
    e_diff=now.date()-end_date
    if (e_diff.days == 0):
        e_diff = "today"
    elif (e_diff.days == 1):
        e_diff = "yesterday"
    else:
        e_diff=str(e_diff.days)+" days ago"
    if start_date > end_date :
        print("Wrong input date!")
    else:
        
        # If get specific range of data, choose whether need to start from a specific page. If not, would begin from the first page.
        # In this part, if you want to get very early data, it can jump faster to the page you need
        print("Do you need to get data start from specific page? (if no, default setting is 10 pages per day.)")
        dn = input("1 - Yes | 2 - No")
        if dn=="2":
            #Set up in default 10 pages per day for scrapping.
            start_page = 0
        elif dn=="1":
            print("Please input the start page and the end page")
            while True:
                try:
                    # Note: Python 2.x users should use raw_input, the equivalent of 3.x's input
                    start_page = int(input("Start from:"))
                except ValueError:
                    print("Your input is not an integer, please try again.")
                    # better try again... Return to the start of the loop
                    continue
                else:
                    # page was successfully parsed!
                    # we're ready to exit the loop.
                    break
elif number=="2":
    s_diff="today"
    e_diff="today"
elif number=="1":
    s_diff="yesterday"
    e_diff="yesterday"
else:
    print("Input Wrong Selection!")
    exit()

label = 1 #mark the label as 1, if first appear end day, label becomes 0. Until last appears start day, label change to 2, and stop.
for j in range(start_page,1000):
    driver = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver")
    # get the url
    url = "https://www.mycareersfuture.sg/search?sortBy=new_posting_date&page=" + str(j)
    driver.get(url)
    time.sleep(5)
    last_post=driver.find_elements_by_name("last_posted_date")
    last=last_post[len(last_post)-2].text
    first=last_post[0].text  
    print(first)
    print(s_diff)
    print(e_diff)
    if (first=="Posted " + e_diff):
        label = 0
    if (first == "Posted today"):
        g_date = now.strftime("%Y-%m-%d")
    elif (first == "Posted yesterday"):
        g_date = (now-timedelta(1)).strftime("%Y-%m-%d")
    else:
        d_diff = re.findall(r'\d+', first)
        d_diff = int("".join(d_diff))
        g_date =(now-timedelta(d_diff)).strftime("%Y-%m-%d")

    if (label == 1):
        driver.quit()
        continue
    else:
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
            company_info=[g_date,company[i].text,job_title[i].text,location[i*2],employment_type[i*2],seniority[i*2],category[i*2].text,salary[3*i],salary[3*i+2]]
            wks.append_row(company_info)
            time.sleep(1)
    
        if (last=='Posted ' + s_diff):
            label = 2

        driver.quit()
        if (label == 2):
            print("Page" + str(i) + "Not Today")
            exit()

