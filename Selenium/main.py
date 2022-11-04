from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import csv
from selenium.webdriver import ActionChains

PATH = "C:\Program Files (x86)\chromedriver.exe"
MAIN_PAGE = "https://www.monster.com.sg/srp/results?sort=1&limit=100&query=information%20systems&searchId=8831318c-251f-4db6-9c7b-24153fef881a"
CACHE_MAIN ="https://webcache.googleusercontent.com/search?q=cache:2JhpnuUJxQcJ:https://www.monster.com.sg/search/information-systems-jobs+&cd=1&hl=en&ct=clnk&gl=sg&searchId=dcc986ae-5d6c-4941-862b-a4aef18364ee"

driver = webdriver.Chrome(PATH)
headers = {"User-Agent":'Chrome/94.0.4606.71'}

#schema
data_dict = {}
data_dict['Jobs'] = []
data_dict['Jobs'].append(
    {
        'job_title': 'Test Title',
        'company': 'Test company',
        'experience': '7-10 Years',
        'salary':'2k',
        'job_description': 'Test Description',
        'skills': ['Skill1','Skill2','Skill3']
    }
)

logs = []

#gets cycle starting from a main page
def cycle():
    time.sleep(3)
    scroll()
    time.sleep(2)
    source = driver.page_source
    soup =BeautifulSoup(source,'lxml')
    links =[]
    link_finder = soup.find_all('h3', class_="medium")
    for link in link_finder:
        ref = link.find('a').get("href")
        links.append(ref)
    for i in range(0,len(links),5):
        if(i+4 < len(links)):
            url1 = "https:"+links[i]
            url2 = "https:"+links[i+1]
            url3 = "https:"+links[i+2]
            url4 = "https:"+links[i+3]
            url5 = "https:"+links[i+4]
            scrape_single(url1,url2,url3,url4,url5)
    clicker()





def scroll():
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

#helper function to scrape a single page
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
    try:
        source = driver.page_source
        soup =BeautifulSoup(source,'lxml')
        skills = []
        yoe='null'
        pay='null'
        title = soup.find('div', class_="job-tittle detail-job-tittle").find('h1').get_text(strip=True)
        company = soup.find('a', class_="under-link").get_text(strip=True)
        
        if(soup.find('div', class_="col-xxs-12 col-sm-3 text-ellipsis").find('span') != None):
            yoe = soup.find('div', class_="col-xxs-12 col-sm-3 text-ellipsis").find('span').get_text(strip=True)
        
        if(soup.find('span', class_="package") != None):
            pay = soup.find('span', class_="package").get_text(strip=True)
        
        skill_link = soup.find_all('span', class_="round-card mb5 grey-link")
        for s in skill_link:
            skill = s.find('a').get_text(strip=True)
            skills.append(skill)

        items = [title,company,yoe,pay,skill]
        data_dict['Jobs'].append(
            {
                'job_title': title,
                'company': company,
                'experience': yoe,
                'salary':pay,
                'skills': skills
            }
        )
        items = [title,company,yoe,pay,skills]
        with open('data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(items)
    except:
        logs.append([driver.current_url])



def clicker():
    time.sleep(1)
    try:
        element = driver.find_elements_by_xpath("//button[@class='btn-next-prev btn-next']")
        actions = ActionChains(driver)
        if len(element) > 1:
            actions.move_to_element(element[1]).perform()
            element[1].click()
            cycle()
        else:
            actions.move_to_element(element[0]).perform()
            element[0].click()
            cycle()
    finally:
        logs.append('Theres no more links to click')
    

PART_TWO='https://www.monster.com.sg/srp/results?start=8100&sort=1&limit=100&query=information%20systems&searchId=8831318c-251f-4db6-9c7b-24153fef881a'
PART_THREE = 'https://www.monster.com.sg/srp/results?start=9600&sort=1&limit=100&query=information%20systems&searchId=8831318c-251f-4db6-9c7b-24153fef881a'    
#now each weblink is stored in the links array what we will do is use sel to open them up
try:
    driver.get(PART_TWO)
    cycle()
finally:
    with open('logs.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(logs)
    with open('data.txt', 'w') as outfile:
        json.dump(data_dict, outfile)
    
    driver.quit()