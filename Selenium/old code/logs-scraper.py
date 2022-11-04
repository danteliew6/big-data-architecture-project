from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import csv
from selenium.webdriver import ActionChains

links =[]
with open('logs_cleaned.csv','r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        links.append(row)

data_dict = {}
data_dict['Jobs'] = []

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
headers = {"User-Agent":'Chrome/94.0.4606.71'}


def scrape_single(weblink1,weblink2,weblink3,weblink4,weblink5):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(weblink1)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(weblink2)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[3])
    driver.get(weblink3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[4])
    driver.get(weblink4)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[5])
    driver.get(weblink5)

    time.sleep(3)
    for i in range(4,-1,-1):
        closer(i)
    

def closer(n):
    scrape()
    driver.close()
    driver.switch_to.window(driver.window_handles[n])


def scrape():
    source = driver.page_source
    soup =BeautifulSoup(source,'lxml')
    skills = []
    yoe='null'
    pay='null'
    jd=''
    title = soup.find('div', class_="job-tittle detail-job-tittle").find('h1').get_text(strip=True)
    company = soup.find('a', class_="under-link").get_text(strip=True)
    
    if(soup.find('span', class_="exp") != None):
        yoe = soup.find('div', class_="col-xxs-12 col-sm-3 text-ellipsis").find('span').get_text(strip=True)
    
    if(soup.find('span', class_="package") != None):
        pay = soup.find('span', class_="package").get_text(strip=True)
    if(soup.find('p', class_="jd-text") != None):
        jd =soup.find('p', class_="jd-text").get_text()

    
    skill_link = soup.find_all('span', class_="round-card mb5 grey-link")
    for s in skill_link:
        skill = s.find('a').get_text(strip=True)
        skills.append(skill)



    data_dict['Jobs'].append(
        {
            'job_title': title,
            'company': company,
            'experience': yoe,
            'salary':pay,
            'job_description':jd,
            'skills': skills
        }
    )
    jd = jd.encode('cp850', errors='replace')
    items = [title,company,yoe,pay,jd,skills]
    with open('log_getter.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(items)

try:
    for i in range(0,len(links),5):
        if(i+4 < len(links)):
            url1 =links[i][0]
            url2 =links[i+1][0]
            url3 =links[i+2][0]
            url4 =links[i+3][0]
            url5 =links[i+4][0]
            scrape_single(url1,url2,url3,url4,url5)
finally:
    with open('data.txt', 'w') as outfile:
        json.dump(data_dict, outfile)
'''
link = 'https://www.monster.com.sg/seeker/job-details?id=3143447&searchId=8831318c-251f-4db6-9c7b-24153fef881a'

driver.get(link)
scrape()
'''
driver.quit()
