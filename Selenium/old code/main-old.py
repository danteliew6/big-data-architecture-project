from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import csv
from selenium.webdriver import ActionChains


#download chrome driver based on your version
#  https://sites.google.com/chromium.org/driver/
# dl based on your chrome browser version and place the file in Program Files (x86)
#C:\Program Files (x86)
PATH = "C:\Program Files (x86)\chromedriver.exe"
MAIN_PAGE = "https://www.monster.com.sg/srp/results?sort=1&limit=100&query=information%20systems&searchId=8831318c-251f-4db6-9c7b-24153fef881a"
CACHE_MAIN ="https://webcache.googleusercontent.com/search?q=cache:2JhpnuUJxQcJ:https://www.monster.com.sg/search/information-systems-jobs+&cd=1&hl=en&ct=clnk&gl=sg&searchId=dcc986ae-5d6c-4941-862b-a4aef18364ee"

driver = webdriver.Chrome(PATH)
headers = {"User-Agent":'Chrome/94.0.4606.71'}

#data Schema
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

#to keep a log of errors
logs = []




#Scoping the Scraping operation:
#1 First we will go into the main page





#helper function to scroll the page
def scroll():
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

#helper function to scrape a single page
def scrape_single(weblink):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(weblink)
    time.sleep(3)
    source = driver.page_source
    soup =BeautifulSoup(source,'lxml')
    skills = []
    try:
        title = soup.find('div', class_="job-tittle detail-job-tittle").find('h1').get_text(strip=True)
        company = soup.find('a', class_="under-link").get_text(strip=True)
        yoe = soup.find('div', class_="col-xxs-12 col-sm-3 text-ellipsis").find('span').get_text(strip=True)
        pay = soup.find('span', class_="package").get_text(strip=True)
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
                'skills': skills
            }
        )
    except:
        logs.append([weblink])


#gets the starting pages
def getNewPage(start):
    driver.get(start)
    time.sleep(5)
    scroll()
    time.sleep(2)
    source = driver.page_source
    soup =BeautifulSoup(source,'lxml')
    links =[]
    link_finder = soup.find_all('h3', class_="medium")
    for link in link_finder:
        ref = link.find('a').get("href")
        links.append(ref)
    for i in range(len(links)):
        url = "https:"+links[i]
        scrape_single(url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    clicker()


def cycle():
    time.sleep(5)
    scroll()
    time.sleep(2)
    source = driver.page_source
    soup =BeautifulSoup(source,'lxml')
    links =[]
    link_finder = soup.find_all('h3', class_="medium")
    for link in link_finder:
        ref = link.find('a').get("href")
        links.append(ref)
    for i in range(len(links)):
        url = "https:"+links[i]
        scrape_single(url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    clicker()


def clicker():
    time.sleep(2)
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
    

    
#now each weblink is stored in the links array what we will do is use sel to open them up
#getNewPage(MAIN_PAGE)


driver.get(MAIN_PAGE)
print(driver.current_url)
logs.append([driver.current_url])
with open('logs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(logs)
with open('data2.txt', 'w') as outfile:
    json.dump(data_dict, outfile)



#2 Here we want to target each card in the page and get the link to each Job








#3 After we go into each job we want to get the relevant details and store themin a JSON
#4 After that go back to the main page and repeat the process till theres no more in the page
#5 Go to the next page and repeat the process


#print(driver.page_source)


#driver.quit()

